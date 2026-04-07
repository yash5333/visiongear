from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['short_id', 'user', 'full_name', 'total', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status']
    list_editable = ['status']
    search_fields = ['user__username', 'full_name', 'email']
    inlines = [OrderItemInline]
    readonly_fields = ['order_id', 'transaction_id', 'created_at']
