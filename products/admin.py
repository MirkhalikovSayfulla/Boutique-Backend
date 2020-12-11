from django.contrib import admin
from .models import (
    Subscribe,
    Category,
    Customer,
    Product,
    ProductView,
    Order,
    OrderItem,
    Brand,
    Type
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'status','completed']
    list_filter = ['type', 'brand', 'category']
    search_fields = ['name']


admin.site.register(Subscribe)
admin.site.register(Customer)
admin.site.register(ProductView)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Brand)
admin.site.register(Type)
