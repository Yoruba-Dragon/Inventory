from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Products

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Define which fields are displayed in the user detail page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('department', 'picture')}),
    )
    
    # Define which fields are displayed when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('department', 'picture')}),
    )
    
    # Optionally, you can add a list_display to show additional fields in the user list
    list_display = ('username', 'email', 'department', 'is_staff', 'is_active')

    # Optionally, you can add search_fields to allow searching by username or email
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Products)
