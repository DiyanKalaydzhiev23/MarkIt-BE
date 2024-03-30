from django.contrib import admin
from file_upload_router.models import Project, UserProfileMedia


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'project_name', 'profile']
    search_fields = ['project_name', 'profile__user__username']


@admin.register(UserProfileMedia)
class UserProfileMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_path', 'extension', 'project']
    search_fields = ['file_path', 'project__project_name']
