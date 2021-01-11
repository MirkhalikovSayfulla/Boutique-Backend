from django.test import SimpleTestCase
from django.urls import resolve, reverse

from products.views import (
    HomeView,
    ShopView,
    Filter,
    ProductDetailView,
    WishlistView,
    CartView,
    CheckoutView,
    add_subscribe,
    add_coupon,
    add_wishlist,
    delete_item,
    add_product,
    update_cart,
    send_mail_checkout
)


class TestUrls(SimpleTestCase):
    #  testing basic urls
    def test_home_url_resolved(self):
        url = reverse('products:home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_shop_url_resolved(self):
        url = reverse('products:shop')
        self.assertEqual(resolve(url).func.view_class, ShopView)

    def test_filtering_url_resolved(self):
        url = reverse('products:filtering', args=['category', 'Watches'])
        self.assertEqual(resolve(url).func.view_class, Filter)

    def test_detail_url_resolved(self):
        url = reverse('products:detail', args=['2'])
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_wishlist_url_resolved(self):
        url = reverse('products:wishlist')
        self.assertEqual(resolve(url).func.view_class, WishlistView)

    def test_cart_url_resolved(self):
        url = reverse('products:cart')
        self.assertEqual(resolve(url).func.view_class, CartView)

    def test_checkout_url_resolved(self):
        url = reverse('products:checkout')
        self.assertEqual(resolve(url).func.view_class, CheckoutView)

    # testing additional urls
    def test_add_subscribe_url_resolved(self):
        url = reverse('products:subscribe')
        self.assertEqual(resolve(url).func, add_subscribe)

    def test_add_coupon_url_resolved(self):
        url = reverse('products:coupon')
        self.assertEqual(resolve(url).func, add_coupon)

    def test_add_wishlist_url_resolved(self):
        url = reverse('products:add-wishlist', args=['3'])
        self.assertEqual(resolve(url).func, add_wishlist)

    def test_delete_item_url_resolved(self):
        url = reverse('products:delitem', args=['wishlist', '3'])
        self.assertEqual(resolve(url).func, delete_item)

    def add_product_url_resolved(self):
        url = reverse('products:add-product', args=['3'])
        self.assertEqual(resolve(url).func, add_product)

    def update_cart_url_resolved(self):
        url = reverse('products:update-cart', args=['add', '3'])
        self.assertEqual(resolve(url).func, update_cart)

    def send_mail_url_resolved(self):
        url = reverse('products:send-mail-checkout')
        self.assertEqual(resolve(url).func, send_mail_checkout)
