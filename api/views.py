import random

from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Meme, MemeTemplate, MemeUser, Rating
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (MemeSerializer, MemeTemplateSerializer,
                             MemeUserSerializer, RatingSerializer,
                             TopMemeSerializer)


class MemeUserViewSet(UserViewSet):

    queryset = MemeUser.objects.all()
    serializer_class = MemeUserSerializer

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        return super().get_permissions()


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

    @action(detail=False, methods=['get'], url_path='random')
    def random_meme(self, request):
        memes = Meme.objects.all()
        if memes.exists():
            meme = random.choice(memes)
            return Response({
                'meme': meme.id,
                'top_text': meme.top_text,
                'bottom_text': meme.bottom_text,
                'template': meme.template.name
            })
        else:
            return Response({'error': 'No memes available'}, status=404)
        
    @action(detail=True, methods=['post'], url_path='rate')
    def rate_meme(self, request, pk=None):
        try:
            meme = self.get_object()
        except Meme.DoesNotExist:
            return Response({'error': 'Meme not found'}, status=404)
        score_value = request.data.get('score') 
        if score_value is None:
            return Response({'error': 'Score value is required'}, status=400)
        try:
            score_value = int(score_value)
            if score_value < 1 or score_value > 5:
                return Response({'error': 'Score must be between 1 and 5'}, status=400)
        except ValueError:
            return Response({'error': 'Invalid score value'}, status=400)
        Rating.objects.create(meme=meme, user=request.user, score=score_value)
        return Response({'message': 'Rating added successfully'}, status=201)
        
    @action(detail=False, methods=['get'], url_path='top')
    def top_memes(self, request):
        top_memes = Meme.objects.order_by('-created_at')[:10]
        serializer = TopMemeSerializer(top_memes, many=True)
        return Response(serializer.data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    


class RandomMemeViewSet(viewsets.ModelViewSet):
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

