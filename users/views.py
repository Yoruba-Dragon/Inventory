from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import ProductsForm, CustomUserCreationForm, PasswordChangingForm, CategoryForm
from .models import Products,Category
from django.contrib.auth.decorators import user_passes_test
from orders.models import Order
from django.http import JsonResponse
from django.db.models import Sum, Count

def home(request):
    return render(request, 'home.html')
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    
    pending_orders = Order.objects.filter( status="Pending").count()
    completed_orders = Order.objects.filter(status="Completed").count()

    # Fetch product quantities
    product_data = Products.objects.all()
    total_products = product_data.aggregate(Sum('product_quantity'))['product_quantity__sum'] or 0

    # Analytics: Top 5 products with the highest quantity
    top_products = Products.objects.order_by('-product_quantity')[:5]

    # Analytics: Total categories
    total_categories = Products.objects.values('category').distinct().count()

    context = {
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_products": total_products,
        "top_products": top_products,
        "total_categories": total_categories,
    }
    return render(request, "admin_dashboard.html", context)


@user_passes_test(is_admin)
def add_product(request):
    if request.method == "POST":
        form =ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            category_id = request.POST.get("category")
            try:
                category = Category.objects.get(id=category_id)
                product.category = category  # Assign the selected category
                product.save()
                return redirect("admin_dashboard")  # Redirect after successful save
            except Category.DoesNotExist:
                form.add_error("category", "Selected category does not exist.")
        else:
            return render(request, "add_product.html", {"form": form, "categories": Category.objects.all()})
    else:
        form = ProductsForm()
    return render(request, "add_product.html", {"form": form, "categories": Category.objects.all()})
    

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
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form =CustomUserCreationForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)  # Restrict to admin users
def add_category_ajax(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return JsonResponse({"success": True, "category_name": category.name, "category_id": category.id})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "message": "Invalid request."})
@user_passes_test(lambda u: u.is_staff)
def delete_category_ajax(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"success": True, "category_id": category_id})
        except Category.DoesNotExist:
            return JsonResponse({"success": False, "errors": "Category not found."})
    return JsonResponse({"success": False, "errors": "Invalid request method."})
