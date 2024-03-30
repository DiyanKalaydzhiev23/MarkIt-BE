from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from auth_app.models import User, Profile


class UserAdmin(BaseUserAdmin):
    # Define admin model for custom User model with no email field
    list_display = ('username', 'is_staff', 'date_joined')  # Adjust as needed
    list_filter = ('is_staff',)  # Removed 'is_active' from here
    search_fields = ('username',)
    ordering = ('username',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
