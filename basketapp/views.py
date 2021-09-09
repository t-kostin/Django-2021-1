from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from basketapp.models import Basket
from mainapp.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import F, Q


@login_required(login_url='/auth/login/')
def basket(request):
    title = 'корзина'
    items = Basket.objects.filter(user=request.user)\
        .order_by('product__category')

    context = {
        'title': title,
        'items': items,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)
    # basket.quantity += 1
    # basket.save()
    basket.quantity = F('quantity') + 1
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        items = Basket.objects.filter(user=request.user)\
            .order_by('product__category')
        context = {
            'items': items,
        }
        result = render_to_string(
            'basketapp/includes/inc_basket_list.html',
            context
        )
        return JsonResponse({'result': result})
