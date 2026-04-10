# from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.catalog.models import Album, Artist, Song, Genre
from apps.catalog.serializers import AlbumSerializer, ArtistSerializer, SongSerializer, GenreSerializer

# Create your views here.


# Tasks:
#1. get artist with all albums
#2. get all artists
#3. get album with all songs
#4. get all albums from selected genre


class ArtistViewSet(ReadOnlyModelViewSet):
    """Get artist with all albums"""
    queryset = Artist.objects.prefetch_related('albums')
    serializer_class = ArtistSerializer

    def perform_create(self, serializer):
        """Save the owner atribute when creating an artist."""
        serializer.save(owner=self.request.user)


class GenreViewSet(ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

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

    def get_queryset(self):
        """Get all albums from selected artist"""
        queryset = super().get_queryset()
        artist_id = self.request.query_params.get('artist')

        if artist_id is not None:
            queryset = queryset.filter(artist_id=artist_id)

        return queryset
    
    def perform_create(self, serializer):
        """Save the owner atribute when creating an album."""
        serializer.save(owner=self.request.user)


class SongViewSet(ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        """Get all songs from selected album"""
        queryset = super().get_queryset()
        album_id = self.request.query_params.get('album')

        if album_id is not None:
            queryset = queryset.filter(album_id=album_id)

        return queryset
    
    def perform_create(self, serializer):
        """Save the owner atribute when creating a song."""
        serializer.save(owner=self.request.user)