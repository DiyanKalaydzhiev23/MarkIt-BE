from django.db import models
from auth_app.models import Profile


class UserProfileMedia(models.Model):
    project_name = models.CharField(
        max_length=255,
    )
    file_path = models.CharField(
        max_length=255
    )
    extension = models.CharField(
        max_length=10
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='media'
    )
