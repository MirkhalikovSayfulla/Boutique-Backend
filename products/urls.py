from django.urls import path

from rest_framework import routers

from . import views
from .api import (
    CustomerViewSet,
    SubscribeViewSet,
    CategoryViewSet,
    TypeViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductViewsViewSet,
    CouponViewSet, OrderViewSet, WishlistViewSet
)

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),

    path('shop/', views.ShopView.as_view(), name="shop"),
    path('filtering/<str:t>/<str:name>/', views.Filter.as_view(), name="filtering"),
    path('product/<str:pk>/', views.ProductDetailView.as_view(), name="detail"),

    path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),

    path('subscribe/', views.add_subscribe, name="subscribe"),
    path('coupon/', views.add_coupon, name="coupon"),
    path('add-wishlist/<str:product_id>/', views.add_wishlist, name="add-wishlist"),
    path('delete-item/<str:action>/<str:pk>/', views.delete_item, name="delitem"),
    path('add-product/<str:product_id>/', views.add_product, name="add-product"),
    path('update-cart/<str:action>/<str:item_id>/', views.update_cart, name="update-cart"),
    path('send-mail/', views.send_mail_checkout, name='send-mail-checkout'),
]

# API
router = routers.DefaultRouter()
router.register('api/customer', CustomerViewSet, 'customer')
router.register('api/subscribe', SubscribeViewSet, 'subscribe')
router.register('api/category', CategoryViewSet, 'category')
router.register('api/type', TypeViewSet, 'type')
router.register('api/brand', BrandViewSet, 'brand')
router.register('api/product', ProductViewSet, 'product')
router.register('api/productview', ProductViewsViewSet, 'productview')
router.register('api/coupon', CouponViewSet, 'coupon')
router.register('api/order', OrderViewSet, 'order')
router.register('api/wishlist', WishlistViewSet, 'wishlist')


urlpatterns += router.urls
