from django.contrib import admin
from .models import Product, Cart, Order, OrderItem, ContactMessage, ProductImage, Review

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductImage)
admin.site.register(ContactMessage)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'content', 'is_approved')  # ✅ use 'content'
    list_filter = ('is_approved', 'rating', 'product')
    search_fields = ('user__username', 'product__name', 'content')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'tracking_number', 'date_ordered']
    readonly_fields = ['tracking_number']  # So admin can't edit it



