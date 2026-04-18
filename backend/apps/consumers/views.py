from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from apps.consumers.serializers import ConsumerProfileSerializer
from apps.consumers.models import ConsumerProfile


# Create your views here.


class ConsumerProfileView(APIView):
    def get(self, request, user_id):
        profile = get_object_or_404(ConsumerProfile, user_id=user_id)
        serializer = ConsumerProfileSerializer(profile)
        return Response(serializer.data)