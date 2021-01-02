from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('shop/', views.Shop.as_view(), name="shop"),
    path('filtering/<str:t>/<str:name>/', views.Filter.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name="detail"),
    path('wishlist/', views.Wishlist.as_view(), name="wishlist"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('subscribe/', views.add_subscribe, name="subscribe"),
    path('coupon/', views.add_coupon, name="coupon"),
]
