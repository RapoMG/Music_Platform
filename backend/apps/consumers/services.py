from django.db import transaction, models
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from apps.catalog.models import Song, Album
from apps.consumers.models import LibraryItem, PlaylistItem, Playlist

# here comes the business logic (It's not a view, it's a service!)

def add_to_library(user, song: Song) -> tuple[LibraryItem, bool]:
    """Add a song to a user's library. Safely handles duplicate entries."""
    obj, created = LibraryItem.objects.get_or_create(user=user, song=song)
    # get_or_create
    # It retrieve an existing object that matches the parameters or create a new one if it doesn't exist.
    # Returns a tuple of (object, created); created is a boolean that indicates whether the object was created.
    return obj, created

@transaction.atomic
def add_album_to_library(user, album: Album) -> list[LibraryItem]:
    """Add an album to a user's library. Safely handles duplicate entries."""

    songs = album.songs.all()
    creted_items = []

    for song in songs:
        obj , created = add_to_library(user, song)

        if created:
            creted_items.append(obj)

    return creted_items

####### Playlist services #######

def add_song_to_playlist(user, song: Song, playlist: Playlist) -> PlaylistItem:
    """Add a song to a playlist. Safely handles duplicate entries."""

    if not LibraryItem.objects.filter(user=user, song=song).exists():
        raise Exception("Song not in user library")

    # Get the last position of the playlist (only value, not object)
    last_position = PlaylistItem.objects.filter(playlist=playlist).aggregate(models.Max('position'))['position_max'] or 0
    
    return PlaylistItem.objects.create(playlist=playlist, song=song, position=last_position + 1)
    
@transaction.atomic
def remove_song_from_playlist(user, item_id: int, playlist: Playlist) -> None:
    """Remove a playlist item from a playlist."""

    # Get the playlist items in order with race condition prevention 
    items = PlaylistItem.objects.select_for_update().filter(playlist_id=playlist.id, playlist__user=user)

    # Get the last position of the playlist (only value, not object)
    max_position = items.aggregate(models.Max('position'))['position_max'] or 0

    try:
        item = items.get(id=item_id) # item that will be removed
        deleted_position = item.position
        item.delete()
    except PlaylistItem.DoesNotExist:
        raise Exception("Item not found")
    
    # move the items up the playlist (#6 -> #3)
    if deleted_position == max_position:
        return
    
    items.filter(
        position__gt=deleted_position,  # all items after the deleted item
        ).update(position=models.F('position') - 1)

    return

@transaction.atomic
def move_song_in_playlist(user, item_id: int, playlist_id: int, new_position: int) -> PlaylistItem:
    """Move a song in a playlist."""
    
    # Get the playlist items in order with race condition prevention 
    items = PlaylistItem.objects.select_for_update().filter(playlist_id=playlist_id, playlist__user=user)

    try:
        item = items.get(id=item_id) # item that will be moved
    except PlaylistItem.DoesNotExist:
        raise Exception("Item not found")

    old_position = item.position

    if new_position == old_position:
        return item

    max_position = items.aggregate(models.Max('position'))['position_max'] or 0

    if new_position < 1 or new_position > max_position:
        raise Exception("Invalid position")

    # move the item down the playlist (#3 -> #6)
    if new_position > old_position:
        items.filter(
            position__gt=old_position,  # all items after the moved item
            position__lte=new_position  # all items before the new position
            ).update(position=models.F('position') - 1)  # F refer to the value of a model field within a query.

    # move the item up the playlist (#3 -> #1)
    if new_position < old_position:
        items.filter(
            position__lt=old_position,  # all items before the moved item
            position__gte=new_position  # all items after the new position
            ).update(position=models.F('position') + 1)

    # update the moved item
    item.position = new_position

    if new_position > max_position:
        item.position = max_position + 1

    item.save()

    return item
    

# Global services

def get_latest_library_items(limit=12):
    """Return the latest songs added to libraries across users."""
    return (
        LibraryItem.objects
        .select_related('song', 'song__album', 'song__album__artist')
        .order_by('-added_at')[:limit]
    )


def get_latest_library_item():
    """Backward-compatible helper used by older code paths."""
    return get_latest_library_items(limit=1).first()


def get_most_popular_albums(limit=8, days=30):
    """Return albums with the highest number of library additions in a time window."""
    since = timezone.now() - timedelta(days=days)
    return (
        Album.objects
        .filter(songs__owned_by__added_at__gte=since)
        .select_related('artist')
        .annotate(popularity=Count('songs__owned_by'))
        .order_by('-popularity', '-id')[:limit]
    )


def get_newest_albums(limit=5):
    """Return the newest albums in the database."""
    return Album.objects.select_related('artist').order_by('-id')[:limit]


def get_trending_songs(limit=5, days=7, hours=0):
    """
    Returns most added songs in a time window.
    """
    since = timezone.now() - timedelta(days=days, hours=hours)

    return (
        LibraryItem.objects
        .filter(added_at__gte=since)
        .values(
            'song',
            'song__title',
            'song__album__title',
            'song__album__artist__name'
        )
        .annotate(add_count=Count('id'))
        .order_by('-add_count')[:limit]
    )
