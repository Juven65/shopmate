from django.shortcuts import render, redirect
from .models import Product, Cart, Order, OrderItem, Review, ContactMessage, Profile, ShippingAddress
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import login
from .forms import ProductForm, ContactForm, UserUpdateForm, OrderTrackingForm, ProfileForm, ReviewForm, StockUpdateForm, AdminReplyForm, ShippingAddressForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum, Count
from django.db.models import Avg, Q
import calendar
import csv
from weasyprint import HTML
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Count, Sum
from django.utils.timezone import localtime
from django.utils import timezone
from django.utils.safestring import mark_safe
import json




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # 🔐 Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used. Please use another.")
            return redirect('register')

        # ✅ Create inactive user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activate your ShopMate account'
        message = render_to_string('store/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email_msg = EmailMessage(mail_subject, message, to=[email])
        email_msg.content_subtype = "html"  # 🔥 Tell Django it's HTML
        email_msg.send()

        return render(request, 'store/email_sent.html')

    return render(request, 'store/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'store/activation_success.html')
    else:
        return render(request, 'store/activation_invalid.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # 🔁 Redirect based on role
            if user.is_staff:
                return redirect('admin-dashboard')  # admin → dashboard
            else:
                return redirect('product-list')     # normal user → shop
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def product_list(request):
    query = request.GET.get('q')  # "q" is for search query
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if stock is available
    if product.stock == 0:
        messages.error(request, "This product is out of stock.")
        return redirect('product-list')

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    # Prevent exceeding stock
    if cart_item.quantity >= product.stock:
        messages.warning(request, "You cannot add more than available stock.")
    else:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Added to cart.")

    return redirect('product-list')

@login_required
def view_cart(request):
    if request.method == 'POST' and 'update_cart' in request.POST:
        print("POST request received:", request.POST)
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            quantity = request.POST.get(f'quantity_{item.id}')
            print(f'Updating item {item.id} to quantity {quantity}')
            if quantity is not None and quantity.isdigit():
                item.quantity = int(quantity)
                item.save()

        # ✅ Success message (once only)
        messages.success(request, "Cart updated successfully!")
        return redirect('view-cart')  # this is OK, since POST is done

    # ✅ GET request handling (needed!)
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity

    total = sum(item.subtotal for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })



@login_required
@require_POST
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('view-cart')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product, is_approved=True)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    form = None  # default value
    existing_review = None  # ✅ make sure it's defined

    if request.user.is_authenticated:
        existing_review = product.reviews.filter(user=request.user).first()

        if request.method == 'POST':
            if existing_review:
                messages.warning(request, "You've already reviewed this product.")
            else:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.product = product
                    review.user = request.user
                    review.save()
                    messages.success(request, "Review submitted!")
                    return redirect('product-detail', product_id=product.id)
        else:
            if not existing_review:
                form = ReviewForm()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,
        'existing_review': existing_review,  # ✅ now always defined
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list')  # or wherever you want to go
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping_fee = 50
    grand_total = subtotal + shipping_fee
    payment_method = request.POST.get('payment_method')

    # Get or create shipping address for the user
    shipping_address = ShippingAddress.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()

            # Create order with shipping info
            order = Order.objects.create(
                user=request.user,
                name=request.user.get_full_name() or request.user.username,
                address=shipping.address_line,
                phone=shipping.phone_number,
                total_price=grand_total,
                payment_method=payment_method,
            )

            # Create order items and update stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                product = item.product
                product.stock -= item.quantity
                product.save()

                item.delete()

            messages.success(request, "✅ Order placed successfully!")
            return redirect('order-history')
    else:
        form = ShippingAddressForm(instance=shipping_address)

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping_fee,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')

    # Filter
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    if selected_month:
        orders = orders.filter(date_ordered__month=int(selected_month))
    if selected_year:
        orders = orders.filter(date_ordered__year=int(selected_year))

    # Months: (1, 'January') ...
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    years = [y for y in range(2023, datetime.now().year + 1)]

    return render(request, 'store/order_history.html', {
        'orders': orders,
        'months': months,
        'years': years,
        'selected_month': selected_month,
        'selected_year': selected_year,
    })

@login_required
def export_orders_csv(request):
    # Get filtered values
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Filter orders
    orders = Order.objects.filter(user=request.user)
    if selected_month:
        orders = orders.filter(date_ordered__month=selected_month)
    if selected_year:
        orders = orders.filter(date_ordered__year=selected_year)

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date Ordered', 'Product Name', 'Quantity', 'Price', 'Total Price'])

    for order in orders:
        for item in order.items.all():
            writer.writerow([
                order.date_ordered.strftime('%Y-%m-%d %H:%M'),
                item.product.name,
                item.quantity,
                item.price,
                order.total_price
            ])

    return response

@login_required
def export_orders_pdf(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    orders = Order.objects.filter(user=request.user)

    # Check kung valid integer before filtering
    if selected_month and selected_month.isdigit():
        orders = orders.filter(date_ordered__month=int(selected_month))
    if selected_year and selected_year.isdigit():
        orders = orders.filter(date_ordered__year=int(selected_year))

    html_string = render_to_string('store/pdf_template.html', {
        'orders': orders,
        'user': request.user
    })

    html = HTML(string=html_string)
    result = html.write_pdf()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_history.pdf"'
    response.write(result)
    return response

@staff_member_required
def admin_dashboard(request):
    tz = timezone.get_current_timezone()  # Asia/Manila timezone

    # ====== Basic Stats ======
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = (
        Order.objects.filter(status="Delivered")
        .aggregate(total=Sum('total_price'))['total'] or 0
    )

    # ====== Orders per Month (ALL ORDERS) ======
    monthly_orders = (
        Order.objects.annotate(month=TruncMonth('created_at', tzinfo=tz))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    order_months = [item['month'].strftime('%b') for item in monthly_orders if item['month']]
    order_counts = [item['count'] for item in monthly_orders]

    # ====== Monthly Sales (Delivered Orders Only) ======
    monthly_sales = (
        Order.objects.filter(status="Delivered")
        .annotate(month=TruncMonth("created_at", tzinfo=tz))
        .values("month")
        .annotate(total=Sum("total_price"))
        .order_by("month")
    )
    months = [
        calendar.month_name[item["month"].month] if item["month"] else "Unknown"
        for item in monthly_sales
    ]
    sales = [float(item["total"]) for item in monthly_sales]

    # Order Status Counts
    pending_count = Order.objects.filter(status="Pending").count()
    processing_count = Order.objects.filter(status="Processing").count()
    shipped_count = Order.objects.filter(status="Shipped").count()
    delivered_count = Order.objects.filter(status="Delivered").count()

    # ====== Debug Print to Terminal ======
    print("=== Orders Per Month ===", order_months, order_counts)
    print("=== Monthly Sales ===", months, sales)

    # ====== Stock Filter ======
    stock_filter = request.GET.get('stock_filter')
    if stock_filter == "low":
        products = Product.objects.filter(stock__lt=10, stock__gt=0)
    elif stock_filter == "zero":
        products = Product.objects.filter(stock=0)
    else:
        products = Product.objects.all()

    # ====== Send to Template ======
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'products': products,
        'order_months': json.dumps(order_months),
        'order_counts': json.dumps(order_counts),
        'months': json.dumps(months),
        'sales': json.dumps(sales),
        'stock_filter': stock_filter,
        'delivered_count': delivered_count,
        'pending_count': pending_count,
        'processing_count': processing_count,
        'shipped_count': shipped_count,

    }
    return render(request, 'store/admin_dashboard.html', context)

@login_required
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock updated successfully!')
            return redirect('admin-dashboard')  # or wherever you list products
    else:
        form = StockUpdateForm(instance=product)

    return render(request, 'store/update_stock.html', {'form': form, 'product': product})


@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-date_ordered')
    return render(request, 'store/manage_orders.html', {
        'orders': orders
    })

@staff_member_required
@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in ['Pending', 'Processing','Shipped', 'Delivered']:
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.id} updated to {new_status}")
    else:
        messages.error(request, "Invalid status.")
    return redirect('manage-orders')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email to admin
            send_mail(
                subject=f"New Contact Message: {contact.subject}",
                message=f"From: {contact.name} <{contact.email}>\n\n{contact.message}",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=['juvenpinoy@gmail.com'],  # ← change to your actual email
                fail_silently=False,
            )

            contact.is_read = True
            contact.save()

            messages.success(request, "✅ Message sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})

@staff_member_required
def manage_reviews(request):
    reviews = Review.objects.select_related('product', 'user').order_by('-created_at')
    return render(request, 'store/manage_reviews.html', {'reviews': reviews})


@staff_member_required
@require_POST
def delete_review(request, review_id):
    from .models import Review
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, "✅ Review deleted.")
    return redirect('manage-reviews')

def admin_search(request):
    category = request.GET.get('category')
    query = request.GET.get('query')
    results = []

    if category == 'product':
        results = Product.objects.filter(name__icontains=query)
        template = 'store/search_product.html'

    elif category == 'user':
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        template = 'store/search_user.html'

    elif category == 'order':
        results = Order.objects.filter(
            Q(id__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(items__product__name__icontains=query)
        ).distinct()
        template = 'store/search_order.html'

    else:
        return redirect('admin-dashboard')

    return render(request, template, {
        'results': results,
        'query': query,
        'category': category
    })

@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.select_related('product')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Processing', 'Shipped', 'Delivered']:
            order.status = new_status
            order.save()
            messages.success(request, "✅ Order status updated!")
            return redirect('order-detail', order_id=order.id)
        else:
            messages.error(request, "❌ Invalid status")

    return render(request, 'store/order_detail.html', {
        'order': order,
        'items': items
    })

@staff_member_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_orders = Order.objects.filter(user=user).order_by('-date_ordered')

    return render(request, 'store/admin_user_detail.html', {
        'user_detail': user,
        'user_orders': user_orders
    })

@staff_member_required
def manage_contact_messages(request):
    # Load all messages (optional: show recent first)
    messages_qs = ContactMessage.objects.order_by('-created_at')

    # Mark unread messages as read
    messages_qs.filter(is_read=False).update(is_read=True)

    return render(request, 'store/manage_contact_messages.html', {
        'messages': messages_qs
    })

@login_required
def profile_view(request):
    profile = request.user.profile

    # SAFELY fetch shipping address
    existing_shipping = ShippingAddress.objects.filter(user=request.user).first()

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        shipping_form = ShippingAddressForm(request.POST, instance=existing_shipping)

        if profile_form.is_valid() and shipping_form.is_valid():
            profile_form.save()

            shipping = shipping_form.save(commit=False)
            shipping.user = request.user  # always set
            shipping.save()

            messages.success(request, 'Profile and shipping info updated successfully.')
            return redirect('profile')

    else:
        profile_form = ProfileForm(instance=profile)
        shipping_form = ShippingAddressForm(instance=existing_shipping)

    context = {
        'form': profile_form,
        'shipping_form': shipping_form,
        'shipping_address': existing_shipping,
    }
    return render(request, 'store/profile.html', context)



@login_required
def edit_profile(request):
    profile = request.user.profile  # get the current logged-in user's profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Your profile has been updated successfully!')
            return redirect('profile')  # after update, go back to profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'store/edit_profile.html', {'form': form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('product-detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'store/edit_review.html', {'form': form, 'review': review})  # ← ADD `review`


@login_required
def approve_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        review.is_approved = True
        review.save()
        messages.success(request, "Review approved successfully.")
    return redirect('manage-reviews')

@login_required
def delete_my_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, "Your review has been deleted.")
    return redirect('product-detail', product_id=product_id)

@staff_member_required
def reply_to_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        reply = request.POST.get('admin_reply', '')
        review.admin_reply = reply
        review.save()
        messages.success(request, "Reply submitted.")
        return redirect('manage-reviews')

@login_required
def manage_shipping_address(request):
    try:
        address = request.user.shipping_address
    except ShippingAddress.DoesNotExist:
        address = None

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('manage-shipping-address')
    else:
        form = ShippingAddressForm(instance=address)

    return render(request, 'store/manage_shipping_address.html', {
        'form': form,
        'address': address
    })

@login_required
def edit_shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = ShippingAddress(user=request.user)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Shipping address updated successfully!")
            return redirect('profile')  # redirect to profile page after save
    else:
        form = ShippingAddressForm(instance=shipping_address)

    return render(request, 'store/edit_shipping.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.deletion_pending = True
        profile.save()
        request.session['delete_user_id'] = request.user.id

        messages.success(request, mark_safe(
            'Your account will be deleted in <strong>5 seconds</strong>. '
            '<a href="/cancel-delete/" class="btn btn-sm btn-warning ms-2">Undo</a>'
        ))
        return redirect('home')

@login_required
def delete_account_confirm(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return redirect('delete_account')  # fallback if GET

@login_required
def cancel_delete(request):
    profile = request.user.profile
    if profile.deletion_pending:
        profile.deletion_pending = False
        profile.save()
        messages.success(request, "Account deletion cancelled.")
    return redirect('profile')

@csrf_exempt
def permanent_delete(request):
    user_id = request.session.get('delete_user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if user.profile.deletion_pending:
                user.delete()
        except User.DoesNotExist:
            pass
    return JsonResponse({'status': 'ok'})

@staff_member_required
def update_tracking_number(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderTrackingForm(request.POST or None, instance=order)

    if form.is_valid():
        form.save()
        return redirect('manage-orders')  # or back to a detail page

    return render(request, 'store/update_tracking.html', {'form': form, 'order': order})
