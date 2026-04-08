from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User
from apps.users.serializers import LoginSerializer, UserSerializer

# Create your views here.

class ConsumerLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["login"],
            password=serializer.validated_data["password"],
            account_type="consumer"
        )

        if not user:
            return Response({"detail": "Invalid credentials"}, status=401)
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "message": "Logged in as consumer"}, status=200)


class UserDetailView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
class ConsumerLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        token = getattr(request.user, 'auth_token', None)
        if token:
            token.delete()
        
        return Response({"message": "Logged out as consumer"}, status=200)
