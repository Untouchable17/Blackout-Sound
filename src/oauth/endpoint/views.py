from django.shortcuts import render
from rest_framework import permissions, generics, parsers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from src.base.permissions import IsAuthor
from src.oauth import serializers
from src.oauth import models


class UserView(APIView):
    """ Просмотр/Редактирование профиля """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        profile = models.AuthUser.objects.get(id=pk)
        serializer = serializers.UserSerializer(profile)

        return Response(serializer.data)

    def post(self, request, pk):
        serializer = serializers.UserSerializer(data=request.data, instance=request.user.profile)
        if serializer.is_valid():
            serializer.save()
        return Response(status=201)


class SocialLinkView(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    serializer_class = serializers.SocialLinkSerializer

    def get_queryset(self):
        return self.request.user.profile.social_links.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class ProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        profile = models.AuthUser.objects.get(id=pk)
        serializer = serializers.ProfileSerializer(profile)

        return Response(serializer.data)