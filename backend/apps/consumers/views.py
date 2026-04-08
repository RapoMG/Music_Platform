from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404

from apps.consumers.serializers import ConsumerRegisterSerializer, ConsumerProfileSerializer
from apps.consumers.models import ConsumerProfile
from apps.users.models import User

# Create your views here.

class ConsumerRegisterView(APIView):
    def post(self, request):
        serializer = ConsumerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {   
                "token": token.key,
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "Consumer registered successfully"
            },
            status=status.HTTP_201_CREATED
    )


class ConsumerProfileView(APIView):
    def get(self, request, user_id):
        profile = get_object_or_404(ConsumerProfile, user_id=user_id)
        serializer = ConsumerProfileSerializer(profile)
        return Response(serializer.data)