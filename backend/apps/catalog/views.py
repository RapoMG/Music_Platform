from django.http import FileResponse, Http404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.catalog.models import Album, Artist, Song, Genre
from apps.catalog.serializers import AlbumSerializer, ArtistSerializer, SongSerializer, GenreSerializer

# Create your views here.


class ArtistViewSet(ReadOnlyModelViewSet):
    """Get artist with all albums"""
    queryset = Artist.objects.prefetch_related('albums')
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]


class GenreViewSet(ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Get all albums from selected genre"""
        queryset = super().get_queryset()
        genre_id = self.request.query_params.get('genre')

        if genre_id is not None:
            queryset = queryset.filter(genre_id=genre_id)

        return queryset


class AlbumViewSet(ReadOnlyModelViewSet):
    queryset = Album.objects.prefetch_related('songs')
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Get all albums from selected artist"""
        queryset = super().get_queryset()
        artist_id = self.request.query_params.get('artist')

        if artist_id is not None:
            queryset = queryset.filter(artist_id=artist_id)

        return queryset


class SongViewSet(ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def _open_song_file(song: Song):
        """
        Open a song file, tolerating legacy DB paths that incorrectly include
        the ``media/`` prefix even though MEDIA_ROOT already points there.
        """
        field = song.file
        candidates = [field.name]

        if field.name.startswith("media/"):
            candidates.append(field.name.removeprefix("media/"))

        last_error = None
        for candidate in candidates:
            try:
                return field.storage.open(candidate, "rb")
            except FileNotFoundError as exc:
                last_error = exc

        raise Http404("Audio file not found") from last_error

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated], url_path="audio")
    def audio(self, request, pk=None):
        """Get song audio file by id and stream it to user"""
        song = self.get_object()
        return FileResponse(self._open_song_file(song), as_attachment=False)

    def get_queryset(self):
        """Get all songs from selected album"""
        queryset = super().get_queryset()
        album_id = self.request.query_params.get('album')

        if album_id is not None:
            queryset = queryset.filter(album_id=album_id)

        return queryset
    
