from rest_framework import serializers
from .models import ProjectPrompts


class ProjectPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPrompts
        fields = ['prompt']
