from django.db import transaction
from apps.catalog.models import Song, Album
from apps.consumers.models import LibraryItem

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


    