from django.urls import path
from . import views
from .views import contact_view
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('products/', views.product_list, name='product-list'),
    path('cart/', views.view_cart, name='view-cart'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('product/<int:product_id>/', views.product_detail, name='product-detail'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('order-history/', views.order_history, name='order-history'),
    path('order-history/export/', views.export_orders_csv, name='export-orders'),
    path('order-history/pdf/', views.export_orders_pdf, name='export-orders-pdf'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('update-stock/<int:product_id>/', views.update_stock, name='update-stock'),
    path('manage-orders/', views.manage_orders, name='manage-orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update-order-status'),
    path('manage-reviews/', views.manage_reviews, name='manage-reviews'),
    path('approve-review/<int:review_id>/', views.approve_review, name='approve-review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit-review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete-review'),
    path('contact/', contact_view, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('admin-search/', views.admin_search, name='admin-search'),
    path('reply-to-review/<int:review_id>/', views.reply_to_review, name='reply-to-review'),
    path('admin-orders/<int:order_id>/', views.order_detail, name='order-detail'),
    path('admin/user/<int:user_id>/', views.admin_user_detail, name='admin-user-detail'),
    path('admin-dashboard/user/<int:user_id>/', views.admin_user_detail, name='admin-user-detail'),
    path('contact-messages/', views.manage_contact_messages, name='manage-contact-messages'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('delete-my-review/<int:review_id>/', views.delete_my_review, name='delete-my-review'),
    path('my-address/', views.manage_shipping_address, name='manage-shipping-address'),
    path('edit-shipping/', views.edit_shipping, name='edit-shipping'),
    path('delete_account/', views.delete_account_confirm, name='delete_account'),
    path('delete_account/confirm/', views.delete_account, name='delete_account_confirm'),
    path('cancel-delete/', views.cancel_delete, name='cancel-delete'),
    path('permanent-delete/', views.permanent_delete, name='permanent-delete'),
    # store/urls.py
    path('update-tracking/<int:order_id>/', views.update_tracking_number, name='update-tracking'),
    path('reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='store/password_change.html',
        success_url='/profile/'
    ), name='password_change'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add-product/', views.add_product, name='add-product'),
    path('checkout/', views.checkout, name='checkout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)