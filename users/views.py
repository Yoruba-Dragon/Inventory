from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import ProductsForm, CustomUserCreationForm, PasswordChangingForm
from .models import Products
from django.contrib.auth.decorators import user_passes_test
from orders.models import Order


def home(request):
    return render(request, 'home.html')
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Fetch all orders
    pending_orders = Order.objects.filter(status='pending').order_by('-created_at')
    approved_orders = Order.objects.filter(status='approved').order_by('-created_at')
    rejected_orders = Order.objects.filter(status='rejected').order_by('-created_at')

    # Handle form submissions for approving/rejecting
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = get_object_or_404(Order, id=order_id)

        if action == 'approve':
            if order.quantity <= order.product.product_quantity:
                order.status = 'approved'
                order.product.product_quantity -= order.quantity
                order.product.save()
            else:
                order.status = 'rejected'
        elif action == 'reject':
            order.status = 'rejected'

        order.save()
        return redirect('admin_dashboard')

    # Fetch all products
    products = Products.objects.all()

    context = {
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'rejected_orders': rejected_orders,
        'products': products,
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to the admin dashboard after adding a product
    else:
        form = ProductsForm()

    return render(request, 'add_product.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_staff:  # Check if the user is an admin
                return redirect('admin_dashboard')  # Redirect to the admin dashboard
            else:
                return redirect('dashboard')  # Redirect to the user dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('dashboard')  # Redirect to home after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to home after logout

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangingForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')  # Redirect to home after password change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangingForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})
def dashboard(request):
    return render(request, 'base.html')

