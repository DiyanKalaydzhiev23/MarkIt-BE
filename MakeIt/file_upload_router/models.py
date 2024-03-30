from auth_app.models import Profile
from django.db import models
from auth_app.models import Profile


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.project_name


class UserProfileMedia(models.Model):
    file_path = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='media')

    def __str__(self):
        return f"{self.file_path}.{self.extension}"
