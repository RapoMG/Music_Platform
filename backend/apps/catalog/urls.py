from rest_framework.routers import DefaultRouter

from apps.catalog.views import ArtistViewSet, AlbumViewSet, SongViewSet, GenreViewSet


app_name = 'apps.catalog'

router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'genres', GenreViewSet, basename='genre')



urlpatterns = router.urls

