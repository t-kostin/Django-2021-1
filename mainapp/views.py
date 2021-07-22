from django.shortcuts import render

# Create your views here.

def index(request):
    title = 'товары'
    menu_links = [
        {'href': 'index', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    context = {
        'title': title,
        'menu_links': menu_links,
    }
    return render(request, 'mainapp/products.html', context)