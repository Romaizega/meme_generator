from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import MemeTemplate

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