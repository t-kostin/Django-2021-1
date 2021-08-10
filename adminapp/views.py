from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test


def is_super_user(user):
    return user.is_superuser


@user_passes_test(is_super_user)
def users(request):
    title = 'Пользователи'
    user_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': title,
        'user_list': user_list,
    }
    return render(request, 'adminapp/users.html', context)

@user_passes_test(is_super_user)
def user_create(request):
    title = 'Создать пользователя'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'title': title,
        'update_form': user_form,
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(is_super_user)
def user_update(request, pk):
    title = 'Редактировать пользователя'
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm(instance=user)
    context = {
        'title': title,
        'update_form': user_form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(is_super_user)
def user_delete(request, pk):
    title = 'пользователи/удаление'
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete() # если удаляем из БД
        user.is_active = False # Удаляем установкой флага
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', context)

@user_passes_test(is_super_user)
def categories(request):
    title = 'categories'
    categories_list = ProductCategory.objects.all().order_by('-is_active', 'name')
    context = {
        'title': title,
        'categories': categories_list,
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(is_super_user)
def category_create(request):
    title = 'создание категории'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryEditForm()
    context = {
        'title': title,
        'update_form': category_form,
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(is_super_user)
def category_update(request, pk):
    title = 'редактирование категории'

    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryEditForm(instance=category)
    context = {
        'title': title,
        'update_form': category_form,
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(is_super_user)
def category_delete(request, pk):
    title = 'удаление категории'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        # category.delete() # если удаляем из БД
        category.is_active = False # Удаляем установкой флага
        category.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_to_delete': category,
    }
    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(is_super_user)
def products(request, pk):
    title = 'products of category'
    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category__id=pk).order_by('name')
    context = {
        'title': title,
        'category': category,
        'products': products,
    }
    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
