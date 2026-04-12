from apps.catalog.models import Album, Artist, Song, Genre
from rest_framework import serializers
from rest_framework.permissions import BasePermission, SAFE_METHODS

# Move to custompermissions.py ?
class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # This is safe
            return True
        
        # Write permissions are only allowed to the owner of the object
        owner = getattr(obj, "owner", None)  # obj.owner - None if no owner
        return owner == request.user
        


class ArtistSerializer(serializers.ModelSerializer):
    albums = serializers.StringRelatedField(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Artist
        fields = ['id','name', 'description', 'image', 'albums', 'owner']

    
    
class SongSerializer(serializers.ModelSerializer):
    #album = AlbumSerializer(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Song
        fields = ['id','title', 'file', 'length', 'lyrics', 'author', 'track_no', 'album', 'owner']
        read_only_fields = ['album']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name']


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    #songs = SongSerializer(many=True, read_only=True)
    genre = serializers.StringRelatedField(many=True)
    songs = SongSerializer(many=True, read_only=True)

    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Album
        fields = ['id','title', 'cover', 'release_date', 'published', 'genre', 'artist', 'songs', 'genre', 'owner']

    
