from django.shortcuts import render
from basketapp.models import Basket


def index(request):
    title = 'главная'
    basket = []
    total = 0
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        for element in basket:
            total += element.quantity * element.product.price
    context = {
        'title': title,
        'basket': basket,
        'total': total,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'контакты'
    basket = []
    total = 0
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        for element in basket:
            total += element.quantity * element.product.price
    context = {
        'title': title,
        'basket': basket,
        'total': total,
    }
    return render(request, 'geekshop/contact.html', context)