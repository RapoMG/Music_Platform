from django.urls import path

from apps.consumers.web_views import (
    HomePageView, search_view,
    ArtistListPageView, ArtistDetailPageView, AlbumPageView,
    PlaylistCreateView, UserPlaylistsView, PlaylistEditView,
    GenreListPageView, ArticlesPlaceholderView,
    register, user_login, user_logout, profile_view, profile_edit,
)


app_name = 'apps.consumers_web'

urlpatterns = [
    path('registration/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),

    path('playlist/create/', PlaylistCreateView.as_view(), name='playlist-create'),
    path('playlists/<str:username>/', UserPlaylistsView.as_view(), name='user-playlists'),
    path('playlists/<str:username>/<int:playlist_id>/edit/', PlaylistEditView.as_view(), name='playlist-edit'),

    path('', HomePageView.as_view(), name='home'),

    path('artists/', ArtistListPageView.as_view(), name='artists'),
    path('artists/<int:artist_id>/', ArtistDetailPageView.as_view(), name='artist_details'),

    path('albums/<int:album_id>/', AlbumPageView.as_view(), name='album_details'),

    path('genres/', GenreListPageView.as_view(), name='genres'),
    path('articles/', ArticlesPlaceholderView.as_view(), name='articles'),

    path('search/', search_view, name='search'),
]
