from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import MemeTemplate, User
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import MemeTemplateSerializer, UserSerializer


class UserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class MemeTemplateViewSet(viewsets.ModelViewSet):
    queryset = MemeTemplate.objects.all()
    serializer_class = MemeTemplateSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    @action(
    ['get'],
    detail=False)
    def recived(self, request):
        templates = MemeTemplate.objects.all()
        serializer = MemeTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    @action(
    ['post'],
    detail=False)
    def send(self, request):
        serializer = MemeTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)