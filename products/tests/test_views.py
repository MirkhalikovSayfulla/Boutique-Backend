from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from products.models import (
    Product,
    Brand,
    Category,
    Type,
    Subscribe,
    Coupon,
    Order,
    Wishlist,
    OrderItem
)


class TestView(TestCase):
    def setUp(self) -> None:
        # Client
        self.client = Client()

        # Auth
        self.user = User.objects.create_user(
            'admin', 'admin@gmail.com', 'admin'
        )
        self.client.login(username='admin', password='admin')

        # Urls
        self.home_url = reverse('products:home')
        self.shop_url = reverse('products:shop')
        self.filter_url = reverse(
            'products:filtering',
            args=['category', 'Watches']
        )
        self.product_detail_url = reverse(
            'products:detail', args=['1']
        )
        self.wishlist_url = reverse('products:wishlist')
        self.cart_url = reverse('products:cart')
        self.checkout_url = reverse('products:checkout')
        self.subscribe_url = reverse('products:subscribe')
        self.coupon_url = reverse('products:coupon')
        self.add_wishlist_url = reverse('products:add-wishlist', args=['1'])
        self.delete_item_url = reverse('products:delitem', args=['wishlist', '1'])
        self.add_product_url = reverse('products:add-product', args=['1'])
        self.update_cart_url = reverse('products:update-cart', args=['remove', '1'])

        # Models

        self.brand = Brand.objects.create(
            name='FILA'
        )
        self.category = Category.objects.create(
            name='Watches'
        )
        self.type = Type.objects.create(
            name='Clothes'
        )
        self.product1 = Product.objects.create(
            name='product1',
            price=30.21,
            image='/media/products/product-1.jpg',
            about='very nice product',
            sku=99999,
            brand=self.brand,
            category=self.category,
            description='<h2>All Ok</h2>',
            status='info',
            stars=4,
            completed=False
        )
        self.product1.type.add(self.type)

    def test_home_view_get(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')

    def test_shop_view_get(self):
        response = self.client.get(self.shop_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/shop.html')

    def test_filtering_shop_view_get(self):
        response = self.client.get(self.filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/shop.html')

    def test_product_detail_view_get(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/detail.html')

    def test_wishlist_view_get(self):
        response = self.client.get(self.wishlist_url)
        self.assertEqual(response.status_code, 200)

    def test_cart_view_get(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_get(self):
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)

    def test_subscribe_view_post(self):
        self.client.post(self.subscribe_url, data={
            'email': 'test@gmail.com'
        })
        subscribe = Subscribe.objects.get(id=1)
        self.assertEqual(subscribe.name, 'test@gmail.com')

    def test_add_coupon_view_post(self):
        Coupon.objects.create(
            code='320282',
            discount=30
        )
        self.client.post(self.coupon_url, data={
            'coupon': '320282'
        })
        order = Order.objects.get(id=1)
        self.assertTrue(order.coupon)

    def test_add_wishlist_view_post(self):
        self.client.post(self.add_wishlist_url)
        wishlist = Wishlist.objects.get(id=1)
        self.assertTrue(wishlist)

    def test_delete_item_view_post_and_get(self):
        self.client.post(self.add_wishlist_url)
        self.assertTrue(Wishlist.objects.all())
        self.client.get(self.delete_item_url)
        self.assertFalse(Wishlist.objects.all())

    def test_add_product_view_post(self):
        self.client.post(self.add_product_url, data={
            'quantity': 2
        })
        self.assertTrue(OrderItem.objects.all())

    def test_update_cart_view_post_and_remove(self):
        self.client.post(self.add_product_url, data={
            'quantity': 2
        })
        self.assertEqual(OrderItem.objects.get(id=1).quantity, 2)
        self.client.get(self.update_cart_url)
        self.assertEqual(OrderItem.objects.get(id=1).quantity, 1)
