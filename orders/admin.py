from django.contrib import admin
from .models import Order

@admin.action(description='Approve selected orders')
def approve_orders(modeladmin, request, queryset):
    for order in queryset:
        if order.product.product_quantity >= order.quantity:
            order.product.product_quantity -= order.quantity
            order.product.save()
            order.status = 'Approved'
        else:
            order.status = 'Rejected'
        order.save()

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'created_at')
    actions = [approve_orders]

admin.site.register(Order, OrderAdmin)
