from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('filtering/<str:t>/<str:name>/', views.Filter.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name="detail"),

    path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    
    path('subscribe/', views.add_subscribe, name="subscribe"),
    path('coupon/', views.add_coupon, name="coupon"),
    path('add-wishlist/<int:productid>/', views.add_wishlist, name="add-wishlist"),
    path('delete-item/<str:action>/<int:pk>/', views.delete_item, name="deleteitem"),
]
