from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,Products


admin.site.register(Products)
admin.site.register(UserProfile)

# Register your models here.
