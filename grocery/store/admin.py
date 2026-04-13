from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'unit', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured']
    list_editable = ['price', 'is_available', 'is_featured']
    search_fields = ['name', 'description']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'full_name', 'phone', 'status', 'total_price', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'total_price']
