from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.full_name or self.user.username


class Subscribe(models.Model):
    name = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=299)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=299)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=299)

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_STATUS = (
        (None, 'NONE'),
        ('danger', 'SOLD'),
        ('primary', 'SALE'),
        ('info', 'NEW'),
    )
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='products')
    about = models.TextField()
    sku = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ManyToManyField(Type)
    description = RichTextField()
    status = models.CharField(
        choices=PRODUCT_STATUS,
        default=None, max_length=10,
        null=True, blank=True
    )
    stars = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)]
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""

        return url

    @property
    def get_stars(self):
        stars = []
        for i in range(5):
            if i < self.stars:
                stars.append(True)
            else:
                stars.append(False)
        return stars


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        try:
            return self.product.name
        except:
            return str(self.id)

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""

        return url


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    discount = models.IntegerField()

    def __str__(self):
        return self.code


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.full_name

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return round(total, 2)

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def get_coupon(self):
        if self.coupon:
            return True
        return False


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        try:
            return f'{self.product.name}-{self.order.customer.full_name}'
        except:
            return self.id


class Wishlist(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)

