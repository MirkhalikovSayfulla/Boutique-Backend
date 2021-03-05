from rest_framework import viewsets, permissions

from .models import (
    Customer,
    Subscribe,
    Category,
    Type,
    Brand,
    Product,
    ProductView,
    Coupon,
    Order,
    Wishlist
)
from .serializers import (
    CustomerSerializers,
    SubscribeSerializers,
    CategorySerializers,
    TypeSerializers,
    BrandSerializers,
    ProductSerializers,
    ProductViewSerializers,
    CouponSerializers,
    OrderSerializers,
    WishlistSerializers
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [
        permissions.AllowAny
    ]


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class ProductViewsViewSet(viewsets.ModelViewSet):
    queryset = ProductView.objects.all()
    serializer_class = ProductViewSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [
        permissions.AllowAny
    ]


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializers
    permission_classes = [
        permissions.AllowAny
    ]
