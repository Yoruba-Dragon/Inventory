from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('my-orders/', views.orders_list, name='order_list'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
]
