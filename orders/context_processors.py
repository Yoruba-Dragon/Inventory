from orders.models import Order

def pending_orders_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        pending_orders = Order.objects.filter(status="pending").count()
        return {"pending_orders": pending_orders}
    return {"pending_orders": 0}


def order_notifications(request):
    if request.user.is_authenticated:
        # Get all approved orders that are not completed
        notifications = Order.objects.filter(user=request.user, status='approved', notified=False)
        return {'order_notifications': notifications}
    return {'order_notifications': []}
