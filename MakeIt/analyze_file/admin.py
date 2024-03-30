from django.contrib import admin
from file_upload_router.models import UserProfileMedia


class UserProfileMediaAdmin(admin.ModelAdmin):
    list_display = ('profile', 'file_path', 'extension')
    search_fields = ('profile', 'file_path')
    ordering = ('profile',)


admin.site.register(UserProfileMedia, UserProfileMediaAdmin)
