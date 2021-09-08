import random
from django.shortcuts import render, get_object_or_404
# from json import loads
# 1 from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.core.cache import cache


# def get_basket(user):  # basket now from context processor
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return []

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links.menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():  # Alternative variant of function logic (more DRY)
    if settings.LOW_CACHE:  # if cache activated, try to find product in it
        key = 'products'
        products = cache.get(key)
    else:
        products = None
    if products is None:  # if cache not active or product not found
        products = Product.objects.filter(
            is_active=True,
            category__is_active=True,
        ).select_related('category')
        if settings.LOW_CACHE:  # if cache active, put product in cache
            cache.set(key, products)
    return products


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():  # Alternative variant of function logic
    if settings.LOW_CACHE:  # if cache activated, try to find product in it
        key = 'products_ordered_by_price'
        products = cache.get(key)
    else:
        products = None
    if products is None:  # if cache not active or product not found
        products = Product.objects.filter(
            is_active=True,
            category__is_active=True,
        ).order_by('price')
        if settings.LOW_CACHE:  # if cache active, put product in cache
            cache.set(key, products)
    return products


def get_products_in_category_ordered_by_price(pk):  # Alternative variant logic
    if settings.LOW_CACHE:  # if cache activated, try to find product in it
        key = 'products_in_category_ordered_by_price'
        products = cache.get(key)
    else:
        products = None
    if products is None:  # if cache not active or product not found
        products = Product.objects.filter(
            category__pk=pk,
            is_active=True,
            category__is_active=True,
        ).order_by('price')
        if settings.LOW_CACHE:  # if cache active, put product in cache
            cache.set(key, products)
    return products


def get_hot_product():
    # hot_query = Product.objects.filter(
    #     is_active=True,
    #     category__is_active=True
    # )  # code without caching func
    hot_query = get_products()  # with caching
    return random.sample(list(hot_query), 1)[0]


def get_related_products(product):
    related_products = Product.objects\
            .filter(is_active=True, category__is_active=True)\
            .select_related('category')\
            .exclude(pk=product.pk)[:3]
    return related_products


def products(request, pk=None, page=1):
    title = 'продукты'
    # menu_links = ProductCategory.objects.filter(is_active=True) #  w/o cache
    menu_links = get_links_menu()
    # basket = get_basket(request.user)
    hot_product = get_hot_product()
    related_products = get_related_products(hot_product)

    if pk is not None:
        if pk == 0:
            # without cache
            # products = Product.objects.filter(
            #    is_active=True,
            #    category__is_active=True
            # ).order_by('price')
            products = get_products_ordered_by_price()  # with cache
            category = {
                'name': 'все',
                'pk': 0
            }
        else:
            # without cache
            # category = get_object_or_404(ProductCategory, pk=pk)
            # products = Product.objects.filter(
            #    category__pk=pk,
            #    is_active=True,
            #    category__is_active=True
            # ).order_by('price')  # without cache
            # with cache
            category = get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

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
    # without cache
    # products = Product.objects.filter(is_active=True).order_by('price')
    products = get_products_ordered_by_price()  # with cache
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
    # without cache
    # menu_links = ProductCategory.objects.filter(is_active=True)
    menu_links = get_links_menu()  # with cache
    # basket = get_basket(request.user)
    # product = get_object_or_404(Product, pk=pk)  # without cache
    product = get_product(pk)
    related_products = get_related_products(product)
    context = {
        'title': title,
        'menu_links': menu_links,
        'related_products': related_products,
        # 'basket': basket,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)
