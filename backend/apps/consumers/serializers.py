from rest_framework import serializers

from apps.users.models import User
from apps.users.validators import validate_username_not_email

from apps.consumers.models import ConsumerProfile, LibraryItem

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