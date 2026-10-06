from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'status', 'created_at', 'user')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone', 'user__username')
    inlines = [OrderItemInline]
    actions = ['delete_selected']
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'full_name', 'phone', 'address')
        }),
        ('Order Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')
    actions = ['delete_selected']
