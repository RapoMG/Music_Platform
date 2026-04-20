from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.consumers.views import (
    ConsumerProfileView, UserLibraryView,
    UserPublicPlaylistListView, PublicPlaylistDetailView,
    PlaylistViewSet, PlaylistItemViewSet,
    AddSongToLibraryView, AddAlbumToLibraryView)


app_name = 'apps.consumers'

router = DefaultRouter()
router.register(r'me/playlists', PlaylistViewSet, basename='my-playlists')

urlpatterns = [
    path('consumers/profile/<int:user_id>/', ConsumerProfileView.as_view()),

    path('consumers/library/', UserLibraryView.as_view()),
    path('consumers/library/songs/<int:song_id>/add/', AddSongToLibraryView.as_view()),
    path('consumers/library/albums/<int:album_id>/add/', AddAlbumToLibraryView.as_view()),

    path('users/<str:username>/playlists/', UserPublicPlaylistListView.as_view()),
    path('playlists/<int:pk>/', PublicPlaylistDetailView.as_view()),
    path('', include(router.urls)),

    path(
        'me/playlists/<int:playlist_id>/items/add/',
        PlaylistItemViewSet.as_view({'post': 'add_song'}),
        name='playlist-item-add',
    ),
    path(
        'me/playlists/<int:playlist_id>/items/<int:item_id>/remove/',
        PlaylistItemViewSet.as_view({'delete': 'remove_song'}),
        name='playlist-item-remove',
    ),
    path(
        'me/playlists/<int:playlist_id>/items/<int:item_id>/reorder/',
        PlaylistItemViewSet.as_view({'patch': 'reorder_songs'}),
        name='playlist-item-reorder',
    ),
]

# Aplayer test page url
from apps.consumers.views import player_page
urlpatterns += [
    path('player/', player_page),
]
