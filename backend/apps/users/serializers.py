from rest_framework import serializers

from apps.users.models import User

from apps.consumers.serializers import ConsumerProfileSerializer



class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    consumer_profile = ConsumerProfileSerializer(source='consumerprofile', read_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'account_type', 'consumer_profile', 'id', 'date_joined', 'last_login')
        read_only_fields = ('id', 'email', 'date_joined', 'last_login', )

