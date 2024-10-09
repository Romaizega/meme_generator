from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Meme, MemeTemplate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
    created_by = UserSerializer()
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

    def create(self, validated_data):
        template_data = validated_data.pop('template')
        template = MemeTemplate.objects.get(id=template_data['id'])
        meme = Meme.objects.create(template=template, created_by=self.context['request'].user, **validated_data)
        return meme

