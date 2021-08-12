from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from adminapp.forms import ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
# from django.views.generic import ListView, CreateView, DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin


def is_super_user(user):
    return user.is_superuser


@user_passes_test(is_super_user) # Фунциаональная реализация
def users(request):
    title = 'Пользователи'
    user_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': title,
        'user_list': user_list,
    }
    return render(request, 'adminapp/users.html', context)


# class UserListView(LoginRequiredMixin, ListView):
#     model = ShopUser
#     template_name = 'adminapp/users.html'
#     context_object_name = 'user_list'
#     ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
#
#     # def get_queryset(self): # Альтернатива ordering
#     #     return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     def get_context_data(self):
#         context = super(UserListView, self).get_context_data()
#         title = 'Пользователи'
#         context.update({'title': title})
#         return context


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


# class UserCreateView(LoginRequiredMixin, CreateView):
#     model = ShopUser
#     template_name = 'adminapp/user_update.html'
#     success_url = reverse_lazy('admin_staff:users')
#     form_class = ShopUserRegisterForm
#
#     def get_context_data(self):
#         context = super().get_context_data()
#         title = 'Создать пользователя'
#         context.update({'title': title})
#         return context


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


@user_passes_test(is_super_user)
def product_create(request, pk):
    title = 'создание продукта'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'product_form': product_form,
        'category_pk': pk,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(is_super_user)
def product_read(request, pk):
    title = 'продукт информация'
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'product': product,
    }
    return render(request, 'adminapp/product_read.html', context)

# class ProductDetailView(LoginRequiredMixin, DetailView):
#     model = Product
#     template_name = 'adminapp/product_read.html'


@user_passes_test(is_super_user)
def product_update(request, pk):
    title = 'редактирование продукта'
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[edit_product.category.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'product_form': edit_form,
        'category_pk': edit_product.category.pk,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(is_super_user)
def product_delete(request, pk):
    title = 'удаление продукта'
    product_to_del = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_to_del.is_active = False
        product_to_del.save()
        return HttpResponseRedirect(reverse('admin_staff:products', args=[product_to_del.category.pk]))
    context = {
        'title': title,
        'product_to_del': product_to_del,
    }
    return render(request, 'adminapp/product_delete.html', context)
