from django.shortcuts import render, get_object_or_404
# from json import loads
from mainapp.models import Product, ProductCategory


def products(request, pk=None):
    title = 'продукты'

    # with open('mainapp/menu_links.json', 'r', encoding='utf-8') as source:
    #     menu_links = loads(source.read())

    # menu_links = [
    #     {'href': 'index', 'name': 'все'},
    # ]
    # for element in ProductCategory.objects.all():
    #     menu_links.append({'href': element.href, 'name': element.name})

    menu_links = ProductCategory.objects.all()
    related_products = Product.objects.all()[:3]

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
        }
        return render(request, 'mainapp/products.html', context)

    related_products = Product.objects.all()[:3]
    products = Product.objects.all().order_by('price')

    context = {
        'title': title,
        'menu_links': menu_links,
        'related_products': related_products,
        'products': products,
    }
    return render(request, 'mainapp/products.html', context)
