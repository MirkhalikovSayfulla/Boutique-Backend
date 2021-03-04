from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Customer,
    Subscribe,
    Category,
    Type,
    Brand,
    Product
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
            'completed'
        ]
