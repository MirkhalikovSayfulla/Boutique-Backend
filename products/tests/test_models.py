from django.test import TestCase
from django.contrib.auth.models import User

from products.models import (
    Customer,
    Subscribe,
    Category,
    Type,
    Brand
)


class TestModel(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@gmail.com', 'admin')

    def test_customer_model(self):
        self.assertTrue(Customer.objects.all())

    def test_subscribe_model(self):
        Subscribe.objects.create(
            name='admin@gmail.com'
        )
        s = Subscribe.objects.get(id=1)
        self.assertEquals(s.name, 'admin@gmail.com')

    def test_category_model(self):
        Category.objects.create(
            name='Watches'
        )
        c = Category.objects.get(id=1)
        self.assertEquals(c.name, 'Watches')

    def test_type_model(self):
        Type.objects.create(
            name='Electronics'
        )
        t = Type.objects.get(id=1)
        self.assertEquals(t.name, 'Electronics')

    def test_type_model(self):
        Brand.objects.create(
            name='FILA'
        )
        b = Brand.objects.get(id=1)
        self.assertEquals(b.name, 'FILA')
