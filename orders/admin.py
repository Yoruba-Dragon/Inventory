
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'created_at']

# Register your models here.
