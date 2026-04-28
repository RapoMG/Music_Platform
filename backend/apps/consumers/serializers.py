from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.users.models import User
from apps.users.validators import validate_username_not_email

from apps.consumers.models import ConsumerProfile, LibraryItem, Playlist, PlaylistItem

class ConsumerRegisterSerializer(serializers.ModelSerializer):
    """Serializer for consumer registration."""
    username = serializers.CharField(max_length=150, validators=[validate_username_not_email])
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        read_only_fields = ('id', 'date_joined', 'last_login')

    def validate_username(self, value) -> str:
        validate_username_not_email(value)
        return value

    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            account_type="consumer"
        )

        ConsumerProfile.objects.create(user=user)

        return user


class ConsumerProfileSerializer(serializers.ModelSerializer):
    """Serializer for consumer profile."""
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        #model = User.consumerprofile.related.related_model  # avoid import loop
        model = ConsumerProfile
        fields = ('user','username', 'avatar', 'description', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class LibraryItemSerializer(serializers.ModelSerializer):
    """Serializer for library item."""
    title = serializers.CharField(source='song.title')
    artist = serializers.CharField(source='song.album.artist.name')
    album = serializers.CharField(source='song.album.title')
    file = serializers.FileField(source='song.file')
    length = serializers.DurationField(source='song.length')

    class Meta:
        model = LibraryItem
        fields = ('id', 'title', 'artist', 'album', 'file', 'length', 'added_at')


class PlaylistItemSerializer(serializers.ModelSerializer):
    """Serializer for playlist item with fields prepared for frontend APlayer."""
    name = serializers.CharField(source='song.title')
    artist = serializers.CharField(source='song.album.artist.name')
    url = serializers.SerializerMethodField()
    lrc = serializers.CharField(source='song.lyrics', allow_blank=True, allow_null=True, required=False)
    cover = serializers.SerializerMethodField()

    def get_url(self, obj) -> str | None:
        """Use the authenticated song streaming endpoint for APlayer."""
        request = self.context.get("request")
        if not request:
            return None
        return reverse("apps.catalog:song-audio", kwargs={"pk": obj.song_id}, request=request)

    def get_cover(self, obj) -> str | None:
        """Return an absolute cover URL when a cover exists."""
        cover = getattr(obj.song.album, "cover", None)
        if not cover:
            return None

        try:
            cover_url = cover.url
        except ValueError:
            return None

        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(cover_url)
        return cover_url

    class Meta:
        model = PlaylistItem
        fields = ('name', 'artist', 'url', 'position', 'lrc', 'cover')


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer for playlist."""
    songs_no = serializers.IntegerField(read_only=True, source='items.count')
    class Meta:
        model = Playlist
        fields = ('id','name', 'is_public', 'songs_no')


class PlaylistDetailsSerializer(serializers.ModelSerializer):
    """Serializer for playlist details."""
    items = PlaylistItemSerializer(many=True)
    songs_no = serializers.IntegerField(read_only=True, source='items.count')
    class Meta:
        model = Playlist
        fields = ('id','name', 'description', 'songs_no', 'created_at', 'updated_at',  'items')
        

class AddSongSerializer(serializers.Serializer):
    """Serializer for adding a song to a playlist."""
    song_id = serializers.IntegerField()

class ReorderSongsSerializer(serializers.Serializer):
    """Serializer for reordering a playlist item."""
    position = serializers.IntegerField(min_value=1)

class RemoveSongSerializer(serializers.Serializer):
    """Serializer for removing a song from a playlist."""
    song_id = serializers.IntegerField()
