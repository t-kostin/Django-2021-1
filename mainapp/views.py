from django.shortcuts import render
from json import loads

# Create your views here.

def index(request):

    title = 'продукты'
    with open('mainapp/menu_links.json', 'r', encoding='utf-8') as source:
        menu_links = loads(source.read())

    context = {
        'title': title,
        'menu_links': menu_links,
    }
    return render(request, 'mainapp/products.html', context)