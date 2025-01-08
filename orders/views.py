from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, 'Your order has been submitted.')
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def admin_order_list(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users
    orders = Order.objects.all()
    return render(request, 'orders/admin_order_list.html', {'orders': orders})


@login_required
def update_order_status(request, order_id, status):
    if not request.user.is_staff:
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)

    if status == 'Approved':
        if order.can_approve():
            # Deduct the product quantity
            order.product.product_quantity -= order.quantity
            order.product.save()
            order.status = 'Approved'
            order.save()
            messages.success(request, f'Order approved successfully.')
        else:
            messages.error(request, f'Cannot approve order: Insufficient product quantity.')
    elif status == 'Rejected':
        order.status = 'Rejected'
        order.save()
        messages.success(request, f'Order rejected successfully.')

    return redirect('admin_order_list')
# Create your views here.
