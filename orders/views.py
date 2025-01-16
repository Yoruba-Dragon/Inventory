from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Products
from .forms import OrderForm
from django.core.paginator import Paginator


@login_required
def create_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')

        try:
            product = Products.objects.get(id=product_id)
            quantity = int(quantity)

            if quantity > product.product_quantity:
                messages.error(request, "Insufficient stock for this product. The order has been rejected.")
                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    status='rejected',
                )
            else:
                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    status='pending',
                )
                messages.success(request, "Order created successfully and sent to admin for approval!")
                return redirect('order_list')
        except Products.DoesNotExist:
            messages.error(request, "Invalid product selected.")
        except ValueError:
            messages.error(request, "Invalid quantity.")

    products = Products.objects.all()
    return render(request, 'orders/create_order.html', {'products': products})


@login_required
def orders_list(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Categorize orders by status
    pending_orders = all_orders.filter(status='pending')
    approved_orders = all_orders.filter(status='approved')
    rejected_orders = all_orders.filter(status='Rejected')
    completed_orders = all_orders.filter(status='completed')

    # Notifications for the user: Only approved orders not marked as completed
    notifications = approved_orders.filter(notified=False)

    # Paginate all orders
    paginator = Paginator(all_orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'notifications': notifications,
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'rejected_orders': rejected_orders,
        'completed_orders': completed_orders,
    }

    return render(request, 'orders/orders_list.html', context)



@login_required
def admin_order_list(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users
    orders = Order.objects.all()
    return render(request, 'admin_order_list.html', {'orders': orders})


VALID_STATUSES = ['pending','approved', 'rejected', 'completed']


@login_required
def update_order_status(request, order_id, status):
    if not request.user.is_staff:
        return redirect('home')  # Restrict access to staff users

    order = get_object_or_404(Order, id=order_id)

    status = status.lower()
    if status not in VALID_STATUSES:
        messages.error(request, f'Invalid status "{status}" provided for order #{order.id}.')
        return redirect('admin_order_list')

    if status == 'approved':
        if order.product.product_quantity >= order.quantity:
            order.product.product_quantity -= order.quantity
            order.product.save()
            order.status = 'approved'
            order.notified = False  # Notify the user
            order.save()
            messages.success(request, f'Order #{order.id} approved successfully.')
        else:
            messages.error(request, f'Cannot approve order #{order.id}: Insufficient product quantity.')

    elif status == 'rejected':
        order.status = 'rejected'
        order.notified = False  # Notify the user
        order.save()
        messages.success(request, f'Order #{order.id} rejected successfully.')

    elif status == 'completed':
        if order.status == 'approved':
            order.status = 'completed'
            order.save()
            messages.success(request, f'Order #{order.id} marked as completed.')
        else:
            messages.error(request, f'Order #{order.id} cannot be marked as completed unless it is approved.')

    return redirect('admin_order_list')


@login_required
def merch_list(request):
    products = Products.objects.all()

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': products,
    }

    return render(request, 'merch.html', context)


@login_required
def confirm_order_received(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.status == 'approved':
            order.status = 'completed'
            order.notified = True  # Mark the notification as seen
            order.save()
            messages.success(request, f'Order #{order.id} has been marked as completed.')
        else:
            messages.error(request, f'Order #{order.id} cannot be marked as completed unless it is approved.')

    return redirect('order_list')

