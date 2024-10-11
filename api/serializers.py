from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Meme, MemeTemplate, Rating

User = get_user_model()


class MemeUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )

class MemeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemeTemplate
        fields = (
            'id',
            'name',
            'image_url',
            'default_top_text',
            'default_bottom_text',
        )

    def get_image_url(self, obj):
        return obj.image_url if obj.image_url else None
    

class MemeSerializer(serializers.ModelSerializer):
    template = MemeTemplateSerializer()
    created_by = MemeUserSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Meme
        fields = (
            'id',
            'template',
            'top_text',
            'bottom_text',
            'created_by',
            'created_at',
        )

    @transaction.atomic
    def create(self, validated_data):
        template_data = validated_data.pop('template')
        template = MemeTemplate.objects.get(id=template_data['id'])
        meme = Meme.objects.create(template=template, 
                                   created_by=self.context['request'].user, 
                                   **validated_data)
        return meme


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'id',
            'meme',
            'user',
            'score',
            'created_at')

    
    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        meme = validated_data['meme']
        score = validated_data['score']
        rating, _ = Rating.objects.update_or_create(
            meme=meme, user=user,
            defaults={'score': score}
        )
        return rating
    

class TopMemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ['id', 'top_text', 'bottom_text', 'created_at']