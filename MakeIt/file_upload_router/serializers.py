from rest_framework import serializers
from .models import UserProfileMedia


class UserProfileMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileMedia
        fields = ['file_path', 'extension']
