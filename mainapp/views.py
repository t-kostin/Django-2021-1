from django.shortcuts import render
from json import loads
from mainapp.models import Product, ProductCategory


def index(request):
    title = 'продукты'

    # with open('mainapp/menu_links.json', 'r', encoding='utf-8') as source:
    #     menu_links = loads(source.read())

    menu_links = [
        {'href': 'index', 'name': 'все'},
    ]
    for element in ProductCategory.objects.all():
        menu_links.append({'href': element.href, 'name': element.name})

    products = Product.objects.all()[1:4]
    context = {
        'title': title,
        'menu_links': menu_links,
        'products': products,

    }
    return render(request, 'mainapp/products.html', context)
