from .models import ContactMessage, Review, Order

def new_orders_count(request):
    count = Order.objects.filter(status='Pending').count()
    return {'new_orders_count': count}

def admin_notification_counts(request):
    new_contact_messages = ContactMessage.objects.filter(is_read=False).count()
    new_pending_reviews = Review.objects.filter(is_approved=False).count()
    new_orders = Order.objects.filter(status='Pending').count()

    return {
        'new_contact_messages': new_contact_messages,
        'new_pending_reviews': new_pending_reviews,
        'new_orders': new_orders,
    }