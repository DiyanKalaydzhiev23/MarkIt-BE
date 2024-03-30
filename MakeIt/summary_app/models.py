from django.db import models
from file_upload_router.models import Project, UserProfileMedia


class ProjectPrompts(models.Model):
    prompt = models.TextField()
    file = models.ForeignKey(
        UserProfileMedia,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
