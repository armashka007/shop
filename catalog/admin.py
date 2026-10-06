from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_main')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'old_price', 'stock', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'old_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_active')
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')
    list_filter = ('is_main',)
    search_fields = ('product__name',)
