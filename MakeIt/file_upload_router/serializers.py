from .models import UserProfileMedia
from rest_framework import serializers
from .models import Project


class UserProfileMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileMedia
        fields = ['file_path', 'extension']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'profile']
