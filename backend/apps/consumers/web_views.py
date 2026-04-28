from datetime import timedelta
from collections import defaultdict

from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.urls import reverse
from django.views.generic import TemplateView, CreateView
from django.views.decorators.http import require_POST

from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Q, Count, Prefetch

from apps.consumers.forms import  CustomUserCreationForm, UserUpdateForm, ProfileForm, PlaylistForm
from apps.consumers.services import (
    get_latest_library_items,
    get_most_popular_albums,
    get_newest_albums,
)

from apps.catalog.models import Artist, Album, Song, Genre
from apps.consumers.models import Playlist


User = get_user_model()

# Create your views here.


def format_duration(duration: timedelta) -> str:
    """
    Format timedelta as:
    - MM:SS when hours == 0
    - H:MM:SS when hours > 0
    """
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}:{minutes:02}:{seconds:02}"
    return f"{minutes}:{seconds:02}"


def auth_page_context(*, request, login_form=None, register_form=None):
    """Build context for the shared login/register page."""
    return {
        "login_form": login_form or AuthenticationForm(request),
        "register_form": register_form or CustomUserCreationForm(),
    }

# User views

def register(request):
    """User registration view.
    Uses a custom user creation form that includes email field."""
    # if request includes Post it's bound form, for validation if Post is empty (={}) it's None, an unbound form that don't need validation
    form = CustomUserCreationForm(request.POST or None) # don't need else in if request.POST block

    if request.method == "POST" and form.is_valid(): 
            form.save()
            
            next_url = request.GET.get('next')

            # check if next_url is valid and prevent open redirect vulnerabilities
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("/")  # fallback

    context = auth_page_context(request=request, register_form=form)
    return render(request, "consumers/users/login.html", context)


def user_login(request):
    """User login view.
    Uses Django's built-in AuthenticationForm for validation and authentication.
    """
    form = AuthenticationForm(request, data=request.POST or None) #

    if request.method == "POST" and form.is_valid():
        # This will use the custom authentication backend defined in settings.py to authenticate the user based on username/email and account type.
        # username_or_email = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(request, username=username_or_email, password=password)

        user = form.get_user()
        if user is not None:  # form.is_valid() already checks if user is not None, but we can keep this check for future Form
            login(request, user) # sets user sesion, which makes request.user accesable in whole app

            next_url = request.GET.get('next')  # after login return to prevois page

            # check if next_url is valid and prevent open redirect vulnerabilities
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("/")  # fallback

    context = auth_page_context(request=request, login_form=form)
    return render(request, "consumers/users/login.html", context)

@require_POST
def user_logout(request):
    """User logout view.
    Logs out the user and redirects to the homepage or a specified next URL.
    """
    if request.method == "POST":
        logout(request)
        next_url = request.GET.get('next')  # after login return to prevois page

        # check if next_url is valid and prevent open redirect vulnerabilities
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

    return redirect("/")  # fallback
        
# User profile public view
def profile_view(request, username):
    """User profile view.
    Displays the public profile of a user.
    """

    profile_user = get_object_or_404(User, username=username)
    
    # users playlists that are public
    playlists = profile_user.playlists.filter(is_public=True)
    library = profile_user.library_items.prefetch_related(
        'song__album__artist'    # prefetch songs and albums in library with their artists to avoid N+1 queries
        ).order_by(
            "song__album__artist__name",  # order library items by artist name, then album release date, then song track number
            "song__album__release_date",
            "song__track_no",
            "song__id", # to ensure consistent ordering of songs with same track number in the same album, if there are any
        )

    #albums_groups = defaultdict(list)
    artist_groups_dd = defaultdict(lambda: defaultdict(list))

    # Group library items by artist, album and songs for display in template
    for item in library:
        artist_groups_dd[item.song.album.artist][item.song.album].append(item.song)

    # Convert defaultdict to regular dict for template context
    artist_groups = {artist: dict(albums) for artist, albums in artist_groups_dd.items()}
        

    context = {
        'profile_user': profile_user,
        'playlists': playlists,
        'library': library,
        'artist_groups': artist_groups,
        'form': PlaylistForm(), # form for creating new playlist in profile page, can be used in modal or inline
    }
    return render(request, "consumers/users/profile.html", context)

# User profile edit view
@login_required
def profile_edit(request):
    """User profile edit view.
    Displays and handles the editing of a user's profile.
    """

    profile = request.user.consumerprofile
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    password_form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == "POST":
        if 'save_profile' in request.POST and profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('apps.consumers_web:profile', username=request.user.username)
        
        if 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('apps.consumers_web:profile', username=request.user.username)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'profile': profile,
    }

    return render(request, "consumers/users/profile_edit.html", context)

# Home page view

class HomePageView(TemplateView):
    """Home page view. Displays latest library items, most popular albums, and newest albums."""
    
    template_name = "consumers/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["latest_library_items"] = get_latest_library_items(limit=12)
        context["popular_albums"] = get_most_popular_albums(limit=10, days=30)
        context["newest_albums"] = get_newest_albums(limit=5)

        return context


class ArtistListPageView(TemplateView):
    """Artist list page view. Displays a list of all artists."""

    template_name = "consumers/music/artists.html"

    def get_context_data(self, **kwargs):
        

        context = super().get_context_data(**kwargs)

        # Prefetch albums for each artist, ordered by release date (newest first)
        # and then by id to ensure consistent ordering of albums with the same release date.
        artists = Artist.objects.all().order_by("name").prefetch_related(
            Prefetch(
                "albums",
                queryset=Album.objects.order_by("-release_date", "-id"),
                to_attr="albums_by_newest",
            )
        )

        # Annotate each artist with their latest album (if they have any)
        for artist in artists:
            artist.last_album = artist.albums_by_newest[0] if artist.albums_by_newest else None

        context["artists"] = artists
        return context


class ArtistDetailPageView(TemplateView):
    """Artist detail page view. Displays details of a single artist and their albums."""
    template_name = "consumers/music/artist_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        artist_id = self.kwargs.get('artist_id')
        artist = get_object_or_404(Artist, id=artist_id)
       
        albums = Album.objects.filter(artist=artist, published=True).order_by("-release_date", "-id").all()
        
        # Get all genres associated with the artist's albums in a single query
        genres = Genre.objects.filter(genres__in=albums).distinct()  # distinct to avoid duplicates when an artist has multiple albums in the same genre


        context["artist"] = artist
        context["albums"] = albums
        context["genres"] = genres
        return context


class GenreListPageView(TemplateView):
    """Genre list page view. Displays a list of all genres."""
    template_name = "consumers/music/genres.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all().order_by("name")
        return context


class AlbumPageView(TemplateView):
    """Album detail page view. Displays details of a single album and its songs."""
    template_name = "consumers/music/album_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        album_id = self.kwargs.get('album_id')
        album = get_object_or_404(Album, id=album_id, published=True)
        songs = list(Song.objects.filter(album=album).order_by("track_no").all())

        # sum of song lengths to get total album length
        album_length = sum((song.length for song in songs), start=timedelta())
        # format album length as H:MM:SS or MM:SS
        album_length_display = format_duration(album_length)

        for song in songs:
            song.length_display = format_duration(song.length)

        # Ready to check if the user has the album in their library
        user_library_song_ids = set()
        album_in_library = False

        # Only check if the user is authenticated to avoid unnecessary database queries for anonymous users
        if self.request.user.is_authenticated:
            user_library_song_ids = set(
                self.request.user.library_items.values_list("song_id", flat=True) # get all song ids in user's library as a set for fast lookup
            )
            album_song_ids = {song.id for song in songs}
            album_in_library = bool(album_song_ids) and album_song_ids.issubset(user_library_song_ids)

        context["album"] = album
        context["songs"] = songs
        context["user_library_song_ids"] = user_library_song_ids
        context["album_in_library"] = album_in_library
        context["album_length_display"] = album_length_display
        return context
    

class PlaylistCreateView(LoginRequiredMixin, CreateView):
    """Playlist creation page view. Displays a form to create a new playlist."""

    template_name = "consumers/users/partials/_new_playlist.html"
    model = Playlist
    form_class = PlaylistForm

    def get_success_url(self):
        """After successful playlist creation, redirect to the user's profile page."""
        return reverse('apps.consumers_web:profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        """Set the user of the playlist to the currently logged-in user before saving."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserPlaylistsView(LoginRequiredMixin,TemplateView):
    """User playlists page view. Displays all playlists of a user."""
    template_name = "consumers/users/user_playlists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile_user = get_object_or_404(User, username=self.kwargs.get('username'))

        # Restrictet access to playlists - public playlists are visible thru profile_view
        if self.request.user != profile_user:
            raise PermissionDenied("You cannot view this page.")

        # Playlists with number of the items
        playlists = profile_user.playlists.annotate(items_count=Count('items'))
        
        context['profile_user'] = profile_user
        context['playlists'] = playlists
        return context
    

class ArticlesPlaceholderView(TemplateView):
    template_name = "consumers/articles/articles.html"
    

def search_view(request):
    """Search view.
    Handles search queries for artists, albums, songs
    and users excluding:
     - current user,
     - inactive users,
     - staff users.
    """

    query = (request.GET.get('q') or "").strip()
    artists_res = Artist.objects.none()
    albums_res = Album.objects.none()
    songs_res = Song.objects.none()
    users_res = User.objects.none()

    if query:
        artists_res = Artist.objects.filter(
            Q(name__icontains=query)
        )
        albums_res = Album.objects.filter(
            Q(title__icontains=query)
        )
        songs_res = Song.objects.filter(
            Q(title__icontains=query)
        )
        users_res = User.objects.filter(
            Q(username__icontains=query)
            ).exclude(
                id=request.user.id  # exclude the current user from search results
            ).exclude(
                is_active=False  # exclude inactive users from search results
            ).exclude(
                is_staff=True  # exclude staff users from search results
            )
        
    
    context = {
        'query':query,
        'artists_results': artists_res,
        'albums_results': albums_res,
        'songs_results': songs_res,
        'users_results': users_res,
    }

    return render(request, "consumers/pages/search.html", context)
