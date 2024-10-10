from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Meme, MemeTemplate, Rating, MemeUser
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (MemeSerializer, MemeTemplateSerializer,
                             MemeUserSerializer, RatingSerializer)


class MemeUserViewSet(UserViewSet):

    queryset = MemeUser.objects.all()
    serializer_class = MemeUserSerializer


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
    

class MemeViewSet(viewsets.ModelViewSet):
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def rate_meme(self, request, pk=None):
        try:
            meme = Meme.objects.get(pk=pk)
        except Meme.DoesNotExist:
            return Response({"error": "Meme not found."}, status=status.HTTP_404_NOT_FOUND)
        rating_data = {
            'meme': meme.id,
            'user': request.user.id,
            'score': request.data.get('score')
        }
        serializer = self.get_serializer(data=rating_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)