from django.shortcuts import render
from djoser.views import MemeTemplate, UserViewSet
from rest_framework import viewsets

from api.models import User
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import MemeTemplateSerializer, UserSerializer


class UserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class MemeTemplateViewSet(viewsets.ModelViewSet):
    queryset = MemeTemplate.objects.all()
    serializer_class = MemeTemplateSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)