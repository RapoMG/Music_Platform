from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from django.shortcuts import get_object_or_404

from apps.consumers.serializers import ConsumerProfileSerializer, LibraryItemSerializer
from apps.consumers.models import ConsumerProfile, LibraryItem
from apps.catalog.models import Song, Album
from apps.consumers.services import add_to_library, add_album_to_library


# Create your views here.


class ConsumerProfileView(APIView):
    def get(self, request, user_id) -> Response:
        profile = get_object_or_404(ConsumerProfile, user_id=user_id)
        serializer = ConsumerProfileSerializer(profile)
        return Response(serializer.data)
    

#### Library ####

class AddSongToLibraryView(APIView):
    """Add a song to a user's library."""
    permission_classes = [IsAuthenticated]  # only authenticated users

    def post(self, request, song_id) -> Response:
        try:
            song = Song.objects.get(id=song_id)  # Get the song by ID from the catalog
        except Song.DoesNotExist:
            return Response({"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Add the song to the user's library
        _, created = add_to_library(request.user, song)  # don't care about the object for now

        if created:
            return Response({"message": "Song added to library"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Song already in library"}, status=status.HTTP_400_BAD_REQUEST)
    

class AddAlbumToLibraryView(APIView):
    """Add an album to a user's library."""
    permission_classes = [IsAuthenticated]  # only authenticated users

    def post(self, request, album_id) -> Response:
        try:
            album = Album.objects.get(id=album_id)  # Get the album by ID from the catalog
        except Album.DoesNotExist:
            return Response({"message": "Album not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Add the album to the user's library
        items = add_album_to_library(request.user, album)

        if items:
            # MAybe return the items?
            return Response({"message": "Album added to library"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Album already in library"}, status=status.HTTP_400_BAD_REQUEST)
        

class UserLibraryView(APIView):
    """Get a user's library."""
    serializer_class = LibraryItemSerializer
    permission_classes = [IsAuthenticated]  # only authenticated users

    def get_queryset(self) -> LibraryItem:
        return LibraryItem.objects.filter(user=self.request.user).select_related('song', 'song__album', 'song__album__artist')
        # select_related('song', 'song__album', 'song__album__artist')
        # Follows the foreign key relationships to eager load the related objects.
        