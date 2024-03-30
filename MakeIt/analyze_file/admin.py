from django.contrib import admin
from analyze_file.models import UserProfileMedia


class UserProfileMediaAdmin(admin.ModelAdmin):
    list_display = ('profile', 'file_path', 'extension')
    search_fields = ('profile', 'file_path')
    ordering = ('profile',)


admin.site.register(UserProfileMedia, UserProfileMediaAdmin)
