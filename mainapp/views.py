import random

from django.shortcuts import render, get_object_or_404
# from json import loads
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    hot_query = Product.objects.all()
    return random.sample(list(hot_query), 1)[0]


def get_related_products(product):
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
    return related_products


def products(request, pk=None):
    title = 'продукты'
    menu_links = ProductCategory.objects.all()
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    related_products = get_related_products(hot_product)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
        context = {
            'title': title,
            'menu_links': menu_links,
            'related_products': related_products,
            'category': category,
            'products': products,
            'basket': basket,
            'hot_product': hot_product,
        }
        return render(request, 'mainapp/products.html', context)

    products = Product.objects.all().order_by('price')

    context = {
        'title': title,
        'menu_links': menu_links,
        'related_products': related_products,
        'products': products,
        'basket': basket,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'продукты'
    menu_links = ProductCategory.objects.all()
    basket = get_basket(request.user)
    product = get_object_or_404(Product, pk=pk)
    related_products = get_related_products(product)
    context = {
        'title': title,
        'menu_links': menu_links,
        'related_products': related_products,
        'basket': basket,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)