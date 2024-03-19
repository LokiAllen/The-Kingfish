# Static imports
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

# Non-static imports
from .serializers import UserInfoSerializer
from accounts.models import UserInfo
from mysite import settings

import os

# Create your views here.
def game_view(request):
    response = render(request, 'PenguinGame/index.html')
    response["Cross-Origin-Opener-Policy"] = "same-origin"
    response["Cross-Origin-Resource-Policy"] = "cross-origin"
    response["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response


class GameFileView(View):
    def get(self, request, filename):
        base_path = os.path.join(settings.BASE_DIR, 'static/game')
        file_path = os.path.join(base_path, filename)

        if os.path.exists(file_path):
            file = open(file_path, 'rb')
            response = FileResponse(file)
            response["Cross-Origin-Opener-Policy"] = "same-origin"
            response["Cross-Origin-Resource-Policy"] = "cross-origin"
            response["Cross-Origin-Embedder-Policy"] = "require-corp"

            return response
        else:
            return HttpResponseNotFound("File not found")


class UserData(generics.GenericAPIView):
    serializer_class = UserInfoSerializer
    def get(self, request, *args, **kwargs):
        user_object = User.objects.filter(username__iexact=self.request.user).first()
        if user_object:
            queryset = UserInfo.objects.get(user=user_object)
            serializer = UserInfoSerializer(queryset, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, *args, **kwargs):
        user_object = User.objects.filter(username__iexact=self.request.user).first()
        if not user_object:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user_info_object = UserInfo.objects.get(user=user_object)
        serializer = self.get_serializer(user_info_object, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)