import random
from django.shortcuts import render, get_object_or_404
# from json import loads
# 1 from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 1 def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return []


def get_hot_product():
    hot_query = Product.objects.filter(is_active=True, category__is_active=True)
    return random.sample(list(hot_query), 1)[0]


def get_related_products(product):
    related_products = Product.objects.filter(is_active=True, category__is_active=True, category=product.category)\
            .exclude(pk=product.pk)[:3]
    return related_products


def products(request, pk=None, page=1):
    title = 'продукты'
    menu_links = ProductCategory.objects.filter(is_active=True)
    # basket = get_basket(request.user)
    hot_product = get_hot_product()
    related_products = get_related_products(hot_product)

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            category = {
                'name': 'все',
                'pk': 0
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'menu_links': menu_links,
            'related_products': related_products,
            'category': category,
            'products': products_paginator,
            # 'basket': basket,
            'hot_product': hot_product,
        }
        return render(request, 'mainapp/products.html', context)

    category = {
        'name': 'все',
        'pk': 0
    }
    products = Product.objects.filter(is_active=True).order_by('price')
    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'menu_links': menu_links,
        'related_products': related_products,
        'category': category,
        'products': products_paginator,
        # 'basket': basket,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'продукты'
    menu_links = ProductCategory.objects.filter(is_active=True)
    # basket = get_basket(request.user)
    product = get_object_or_404(Product, pk=pk)
    related_products = get_related_products(product)
    context = {
        'title': title,
        'menu_links': menu_links,
        'related_products': related_products,
        # 'basket': basket,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)