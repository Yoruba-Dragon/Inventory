from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order,Products
from .forms import OrderForm
from users.forms import ProductsForm
from django.contrib.messages import get_messages
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

    # Paginate all orders
    paginator_all = Paginator(all_orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator_all.get_page(page_number)

    # Paginate filtered orders
    pending_orders = Order.objects.filter(user=request.user, status='pending')
    approved_orders = Order.objects.filter(user=request.user, status='approved')
    rejected_orders = Order.objects.filter(user=request.user, status='rejected')

    context = {
        'page_obj': page_obj,
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'rejected_orders': rejected_orders,
        'notifications': all_orders.filter(notified=False, status__in=['approved', 'rejected']),
    }

    return render(request, 'orders/orders_list.html', context)

@login_required
def admin_order_list(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users
    orders = Order.objects.all()
    return render(request, 'admin_order_list.html', {'orders': orders})


@login_required
def update_order_status(request, order_id, status):
    if not request.user.is_staff:
        return redirect('home')  # Restrict access to staff users

    # Retrieve the order
    order = get_object_or_404(Order, id=order_id)

    # Normalize the status input
    status = status.lower()

    # Clear existing messages
    storage = get_messages(request)
    list(storage)  # Consume and clear all messages

    if status == 'approved':
        if hasattr(order, 'can_approve') and callable(order.can_approve):
            print(f"Product Quantity: {order.product.product_quantity}, Order Quantity: {order.quantity}")
            if order.can_approve():
                # Deduct the product quantity
                order.product.product_quantity -= order.quantity
                order.product.save()

                # Update order status
                order.status = 'approved'
                order.save()

                # Success message
                messages.success(request, f'Order #{order.id} approved successfully.')
            else:
                # Error if product quantity is insufficient
                messages.error(request, f'Cannot approve order #{order.id}: Insufficient product quantity.')
                print("Approval failed: Insufficient product quantity")
        else:
            print("Approval failed: can_approve method missing or invalid")
            messages.error(request, "Cannot approve order: Invalid approval logic.")
    elif status == 'rejected':
        # Update order status to rejected
        order.status = 'rejected'
        order.save()

        # Success message
        messages.success(request, f'Order #{order.id} rejected successfully.')
    else:
        # Handle invalid status input
        messages.error(request, f'Invalid status "{status}" provided for order #{order.id}.')

    # Redirect back to the admin order list
    return redirect('admin_order_list')


@login_required
def merch_list(request):

    products= Products.objects.all()

    paginator_all = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator_all.get_page(page_number)

    
    context = {
        'page_obj': page_obj,
        'products': products,
    }

    return render (request, 'merch.html', context)

# def edit_product(request):
    