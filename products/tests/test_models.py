from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from products.models import (
    Brand,
    Category,
    Coupon,
    Customer,
    Order,
    Product,
    ProductImages,
    Subscribe,
    Type,
    OrderItem,
    Wishlist
)


class TestModel(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@gmail.com', 'admin')
        self.brand = Brand.objects.create(
            name='FILA'
        )
        self.category = Category.objects.create(
            name='Watches'
        )
        self.type = Type.objects.create(
            name='Electronics'
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
        self.coupon = Coupon.objects.create(
            code='ABC',
            discount=20
        )
        customer = Customer.objects.get(id=1)
        self.order = Order.objects.create(
            customer=customer,
            coupon=self.coupon,
            complete=False
        )

    def test_customer_model(self):
        self.assertTrue(Customer.objects.all())

    def test_subscribe_model(self):
        Subscribe.objects.create(
            name='admin@gmail.com'
        )
        s = Subscribe.objects.get(id=1)
        self.assertEquals(s.name, 'admin@gmail.com')

    def test_category_model(self):
        c = Category.objects.get(id=1)
        self.assertEquals(c.name, 'Watches')

    def test_type_model(self):
        t = Type.objects.get(id=1)
        self.assertEquals(t.name, 'Electronics')

    def test_brand_model(self):
        b = Brand.objects.get(id=1)
        self.assertEquals(b.name, 'FILA')

    def test_product_model(self):
        self.assertTrue(self.product1)

    def test_product_view_model(self):
        self.assertFalse(ProductImages.objects.all())
        ProductImages.objects.create(
            product=self.product1,
            image='/media/products/product-1.jpg'
        )
        self.assertTrue(ProductImages.objects.all())

    def test_coupon_model(self):
        self.assertTrue(Coupon.objects.all())

    def test_order_model(self):
        self.assertTrue(Order.objects.all())

    def test_order_item_model(self):
        OrderItem.objects.create(
            product=self.product1,
            order=self.order,
            quantity=2,
            date_added=timezone.now()
        )
        self.assertTrue(OrderItem.objects.all())

    def test_wishlist_model(self):
        Wishlist.objects.create(
            product=self.product1,
            order=self.order
        )
        self.assertTrue(Wishlist.objects.all())
