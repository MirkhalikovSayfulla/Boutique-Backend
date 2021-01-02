from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView, ListView, DetailView
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
    new_coupon_code = request.POST.get('coupon')
    order = Order.objects.get(customer=request.user.customer)
    try:
        coupon = Coupon.objects.get(code=new_coupon_code)
    except Exception as err:
        coupon = False
        print(err)
    if order.coupon is None and coupon:
        order.coupon = coupon
        order.save()
    return redirect('products:cart')


def add_wishlist(request, productid):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False
    )
    product = Product.objects.get(id=productid)
    try:
        Wishlist.objects.get(product=product, order=order)
    except:
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
    
