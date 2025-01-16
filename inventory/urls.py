"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views  # Alias for users app views
from orders import views as order_views  # Alias for orders app views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", user_views.home, name='home'),
    path('login/', user_views.login, name='login'),
    path('signup/', user_views.signup, name='signup'),
    path('logout/', user_views.logout_view, name='logout'),
    path('orders/', include('orders.urls')),  # Include orders app URLs
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('admin-dashboard/', user_views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard from orders views
    path('add-product/', user_views.add_product, name='add_product'),  # Add product from orders views
    path('profile/update/', user_views.update_profile, name='update_profile'),
    path("add-category-ajax/", user_views.add_category_ajax, name="add_category_ajax"),
    path("delete-category-ajax/", user_views.delete_category_ajax, name="delete_category_ajax"),
    path('products/edit/<int:pk>/', user_views.edit_product, name='edit_product'),
    
    path('confirm-received/<int:order_id>/', order_views.confirm_order_received, name='confirm_order_received'),
]

# Static and media file handling
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
