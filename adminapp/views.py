from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser


# Create your views here.


def users(request):
    title = 'users'
    user_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
    'title': title,
    'objects': user_list,
    }

    return render(request, 'adminapp/users.html', context)


def user_create(request):
    title = 'create user'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'title': title,
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)
