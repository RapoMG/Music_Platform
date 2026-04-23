from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model # ,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Q

from django.views.generic import TemplateView

from apps.consumers.forms import CustomUserCreationForm, ProfileForm, UserUpdateForm
from apps.consumers.services import (
    get_latest_library_items,
    get_most_popular_albums,
    get_newest_albums,
)

from django.contrib.auth.forms import PasswordChangeForm

from apps.catalog.models import Artist, Album, Song, Genre
from apps.consumers.models import Playlist

User = get_user_model()

# Create your views here.

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
    
    return render(request, 'users/register.html', {'form': form})


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

    return render(request, 'users/login.html', {'form': form})

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
        
    context = {
        'profile_user': profile_user,
        'playlists': playlists,
    }
    return render(request, 'users/profile.html', context)

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

    return render(request, 'users/profile_edit.html', context)

# Home page view

class HomePageView(TemplateView):
    """Home page view. Displays latest library items, most popular albums, and newest albums."""
    
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["latest_library_items"] = get_latest_library_items(limit=12)
        context["popular_albums"] = get_most_popular_albums(limit=10, days=30)
        context["newest_albums"] = get_newest_albums(limit=5)

        return context


class ArtistListPageView(TemplateView):
    """Artist list page view. Displays a list of all artists."""

    template_name = "artists.html"

    def get_context_data(self, **kwargs):
        from django.db.models import Prefetch

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
    template_name = "artist_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        artist_id = self.kwargs.get('artist_id')
        artist = get_object_or_404(Artist, id=artist_id)
        
        context["artist"] = artist
        return context


class GenreListPageView(TemplateView):
    """Genre list page view. Displays a list of all genres."""
    template_name = "genres.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all().order_by("name")
        return context


class ArticlesPlaceholderView(TemplateView):
    template_name = "articles.html"
    
def search_view(request):
    """Search view.
    Handles search queries for artists, albums, and songs."""
    query = (request.GET.get('q') or "").strip()
    artists_res = Artist.objects.none()
    albums_res = Album.objects.none()
    songs_res = Song.objects.none()

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
    
    context = {
        'query':query,
        'artists_results': artists_res,
        'albums_results': albums_res,
        'songs_results': songs_res
    }

    return render(request, 'search.html', context)
