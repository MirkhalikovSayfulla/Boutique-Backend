from django.contrib import admin
from products.models import (
    Subscribe,
    Category,
    Customer,
    Product,
    ProductImages,
    Order,
    OrderItem,
    Brand,
    Type,
    Coupon,
    Wishlist
)
from django.utils.safestring import mark_safe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'status', 'completed']
    list_filter = ['type', 'brand', 'category']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_price']
    search_fields = ['code']

    def discount_price(self, obj):
        return f"${obj.discount}"


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email']
    search_fields = ['user', 'full_name', 'email']


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'get_image']
    search_fields = ['product']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image_url} width="50" heigth="60">')

    get_image.short_description = "Image"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'coupon', 'complete']
    list_filter = ['complete']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'date_added']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'order']
