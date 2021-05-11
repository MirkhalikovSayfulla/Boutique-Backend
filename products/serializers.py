from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Customer,
    Subscribe,
    Category,
    Type,
    Brand,
    Product,
    ProductImages,
    Coupon,
    Order,
    OrderItem,
    Wishlist
)


class CustomerSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Customer
        fields = '__all__'


class SubscribeSerializers(serializers.ModelSerializer):
    name = serializers.EmailField()

    class Meta:
        model = Subscribe
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductImagesSerializers(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )

    brand = serializers.SlugRelatedField(
        queryset=Brand.objects.all(),
        slug_field='name'
    )

    productview_set = ProductImagesSerializers(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image',
            'about',
            'sku',
            'brand',
            'category',
            'type',
            'description',
            'status',
            'get_stars',
            'completed',
            'productview_set'
        ]





class CouponSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(queryset=Customer.objects.all(), slug_field='full_name')

    coupon = serializers.SlugRelatedField(
        queryset=Coupon.objects.all(),
        slug_field='code'
    )

    orderitem_set = OrderItemSerializers(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'coupon',
            'complete',
            'get_cart_total',
            'get_cart_items',
            'get_coupon',
            'orderitem_set'
        ]


class WishlistSerializers(serializers.ModelSerializer):

    product = serializers.StringRelatedField(read_only=True)
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'
