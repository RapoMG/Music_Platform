from apps.consumers.serializers import ConsumerProfileSerializer
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    consumer_profile = ConsumerProfileSerializer(source='consumerprofile', read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('username', 'email', 'account_type', 'consumer_profile', 'id', 'date_joined', 'last_login')
        read_only_fields = ('id', 'email', 'date_joined', 'last_login', )