from django.shortcuts import render
# from basketapp.models import Basket
# from mainapp.views import get_basket


def index(request):
    title = 'главная'
    # basket = get_basket(request.user)
    total = 0
    context = {
        'title': title,
        # 'basket': basket,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'контакты'
    # basket = get_basket(request.user)
    total = 0
    context = {
        'title': title,
        # 'basket': basket,
    }
    return render(request, 'geekshop/contact.html', context)