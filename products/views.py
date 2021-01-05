from django.core.mail import send_mail
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.conf import settings

from products.models import (
    Subscribe,
    Product,
    Category,
    Type,
    Brand,
    Order,
    Coupon,
    Wishlist,
    OrderItem
)


class GetItemsProduct:
    def __init__(self):
        self.request = None

    def get_order(self):
        customer = self.request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        return order

    def get_item(self):
        return self.get_order().orderitem_set.all()

    def get_cart_item(self):
        return self.get_order().get_cart_items

    def get_coupon(self):
        if self.get_order().get_coupon:
            return self.get_order().get_cart_total - self.get_order().coupon.discount
        else:
            return self.get_order().get_cart_total

    def get_wishlist(self):
        return self.get_order().wishlist_set.all()


class GetFiltering:
    def get_brand(self):
        return Brand.objects.order_by('-id')

    def get_types(self):
        return Type.objects.order_by('-id')

    def get_category(self):
        return Category.objects.order_by('-id')


class HomeView(TemplateView, GetItemsProduct):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        context['products'] = Product.objects.filter(
            completed=False).order_by('-id')[:12]
        context['active'] = 'home'
        return context


class ProductDetailView(TemplateView, GetItemsProduct):
    template_name = 'products/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs.get('pk'))
        context['product'] = product
        context['related'] = Product.objects.filter(
            completed=False, category=product.category)[:4]
        return context


class ShopView(ListView, GetFiltering, GetItemsProduct):
    template_name = 'products/shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShopView, self).get_context_data()
        context['active'] = 'shop'
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.GET.getlist('type'):
            queryset = Product.objects.filter(
                Q(type__in=self.request.GET.getlist('type'))
            )

        minprice = self.request.GET.get('minprice', False)
        maxprice = self.request.GET.get('maxprice', False)
        sorting = self.request.GET.get('sorting', False)

        queryset = queryset.filter(completed=False)

        if minprice and maxprice:
            queryset = queryset.filter(
                price__range=(minprice[1:], maxprice[1:]))

        if sorting:
            queryset = queryset.order_by(str(sorting))
        else:
            queryset = queryset.order_by('-id')
        return queryset.distinct()


class Filter(ListView, GetFiltering, GetItemsProduct):
    template_name = 'products/shop.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Filter, self).get_context_data()
        context['active'] = 'shop'
        return context

    def get_queryset(self):
        if self.kwargs.get('t') == 'brand':
            queryset = Product.objects.filter(
                Q(type__in=self.request.GET.getlist('type')) |
                Q(brand__name=self.kwargs['name'])
            )
        elif self.kwargs.get('t') == 'category':
            queryset = Product.objects.filter(
                Q(type__in=self.request.GET.getlist('type')) |
                Q(category__name=self.kwargs['name'])
            )
        else:
            return redirect('products:home')

        minprice = self.request.GET.get('minprice', False)
        maxprice = self.request.GET.get('maxprice', False)
        sorting = self.request.GET.get('sorting', False)

        queryset = queryset.filter(completed=False)

        if minprice and maxprice:
            queryset = queryset.filter(
                price__range=(minprice[1:], maxprice[1:]))

        if sorting:
            queryset = queryset.order_by(str(sorting))
        else:
            queryset = queryset.order_by('-id')

        return queryset.distinct()


class CartView(TemplateView, GetItemsProduct):
    template_name = 'products/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data()
        context['active'] = 'cart'
        return context

    @method_decorator(login_required(login_url='/users/login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class WishlistView(TemplateView, GetItemsProduct):
    template_name = 'products/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data()
        context['active'] = 'wishlist'
        return context

    @method_decorator(login_required(login_url='/users/login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CheckoutView(TemplateView, GetItemsProduct):
    template_name = 'products/checkout.html'

    @method_decorator(login_required(login_url='/users/login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def send_mail_checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    items = order.orderitem_set.all()
    my_product_list = []
    for item in items:
        my_product_list.append(
            f"Product Name: {item.product.name}\nProduct Price: ${item.product.price}\nProduct Quantity: x{item.quantity}\nProduct Total Price: ${item.get_total}\n-----------------\n"
        )
    customer_products = "".join(my_product_list)
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    email = request.POST['email']
    number = request.POST['phone']
    country = request.POST['country']
    city = request.POST['city']
    add1 = request.POST['add1']
    add2 = request.POST['add2']

    send_mail(f'Customer: {first_name} {last_name}',
              f"Request Customer:\nUser Name: {request.user.username}\nFull Name: {request.user.first_name} {request.user.last_name}\nEmail: {request.user.email}\n\nForm Customer:\nFirst Name: {first_name}\nLast Name: {last_name}\nPhone Number: {number}\nEmail: {email}\nCountry: {country}\nCity: {city}\nAddress One: {add1}\nAddress Two: {add2}\n\nProducts: \n-----------------\n{customer_products}\nItems: {order.get_cart_items}\nTotal: ${round(order.get_cart_total, 2)}",
              settings.EMAIL_HOST_USER,
              ['mirxoliqov.sayfulla@gmail.com'],
              fail_silently=False
              )
    return redirect('products:checkout')


def add_subscribe(request):
    try:
        Subscribe.objects.create(
            name=request.POST.get('email')
        )
    except Exception as err:
        print(err)
        return redirect('products:home')
    return redirect("products:home")


def add_coupon(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )
    new_coupon_code = request.POST.get('coupon')
    try:
        coupon = Coupon.objects.get(code=new_coupon_code)
    except Exception as err:
        coupon = False
        print(err)
    if order.coupon is None and coupon:
        order.coupon = coupon
        order.save()
    return redirect('products:cart')


def add_wishlist(request, product_id):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )
    product = Product.objects.get(id=product_id)
    try:
        Wishlist.objects.get(product=product, order=order)
    except Exception as err:
        print(err)
        Wishlist.objects.create(product=product, order=order)
    return redirect('products:wishlist')


def delete_item(request, action, pk):
    if action == 'wishlist':
        Wishlist.objects.get(id=pk).delete()
        return redirect('products:wishlist')
    elif action == 'cart':
        OrderItem.objects.get(id=pk).delete()
        return redirect('products:cart')
    return redirect('products:home')


def add_product(request, product_id):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )
    quantity = request.POST.get('quantity', 1)
    product = Product.objects.get(id=product_id)
    try:
        orderitem = OrderItem.objects.get(product=product, order=order)
        orderitem.quantity = int(orderitem.quantity) + int(quantity)
        orderitem.save()
        return redirect('products:cart')
    except Exception as err:
        OrderItem.objects.create(product=product, order=order, quantity=quantity, date_added=timezone.now())
        print(err)
        print('work except')
    return redirect('products:cart')


def update_cart(request, action, item_id):
    orderitem = OrderItem.objects.get(id=item_id)
    if action == 'add':
        orderitem.quantity = orderitem.quantity + 1
    else:
        orderitem.quantity = orderitem.quantity - 1
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()
    return redirect('products:cart')
