from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Products

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'fullname', 'password', 'department', 'picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password1', 'password2', 'department', 'picture', 'is_staff', 'is_active')}
        ),
    )
    list_display = ('email', 'fullname', 'is_staff', 'is_active')
    search_fields = ('email', 'fullname')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Products)