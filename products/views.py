from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from .models import (
    Subscribe,
    Product,
    Category,
    Type,
    Brand
)


class GetFilterProducts:

    def get_brand(self):
        return Brand.objects.order_by('-id')

    def get_types(self):
        return Type.objects.order_by('-id')

    def get_category(self):
        return Category.objects.order_by('-id')


class Home(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context['products'] = Product.objects.filter(
            completed=False).order_by('-id')
        context['active'] = 'home'
        return context


class Cart(TemplateView):
    template_name = 'products/cart.html'

    def get_context_data(self, **kwargs):
        context = super(Cart, self).get_context_data()
        context['active'] = 'cart'
        return context


class Shop(ListView, GetFilterProducts):
    template_name = 'products/shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Shop, self).get_context_data()
        context['active'] = 'shop'
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.GET.getlist('type'):
            queryset = Product.objects.filter(
                Q(type__in=self.request.GET.getlist('type'))
            )

        minprice = self.request.GET.get('minprice', 0)
        maxprice = self.request.GET.get('maxprice', 0)
        if minprice and maxprice:
            queryset = queryset.filter(price__range=(minprice[1:], maxprice[1:]))
        return queryset.filter(completed=False).order_by('-id')


class Filter(ListView, GetFilterProducts):
    template_name = 'products/shop.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 12

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

        minprice = self.request.GET.get('minprice', 0)
        maxprice = self.request.GET.get('maxprice', 0)
        if minprice and maxprice:
            queryset = queryset.filter(price__range=(minprice[1:], maxprice[1:]))
        return queryset.filter(completed=False).distinct()


def checkout(request):
    return render(request, 'products/checkout.html')


def add_subscribe(request):
    Subscribe.objects.create(
        name=request.POST.get('email')
    )
    return redirect("products:home")
