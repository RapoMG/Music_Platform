from django.db import transaction
from djoser.serializers import UserSerializer, UserCreateSerializer
from apps.consumers.models import ConsumerProfile
from apps.consumers.serializers import ConsumerProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "password")
        # password stays write_only from Djoser base serializer!

    @transaction.atomic
    def create(self, validated_data):
        validated_data["account_type"] = "consumer"
        user = super().create(validated_data)
        ConsumerProfile.objects.get_or_create(user=user)
        return user


class CustomUserSerializer(UserSerializer):
    consumer_profile = ConsumerProfileSerializer(source="consumerprofile", read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "account_type", "consumer_profile", "date_joined", "last_login")
        read_only_fields = fields