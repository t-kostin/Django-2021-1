from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from adminapp.forms import ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'user_list'
    ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']

    # def get_queryset(self): # Альтернатива ordering
    #     return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        title = 'Пользователи'
        context.update({'title': title})
        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    form_class = ShopUserRegisterForm

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        title = 'Создать пользователя'
        context.update({'title': title})
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    # fields = ['first_name'] # Для частичного редактирования полей - перечень названий полей
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        title = 'Редактировать пользователя'
        context.update({'title': title})
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        title = 'удаление пользователя'
        context.update({'title': title})
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'categories'
    ordering = ['-is_active', 'name']

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        title = 'Категории товаров'
        context.update({'title': title})
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        title = 'Создать категорию'
        context.update({'title': title})
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        title = 'Редактировать категорию'
        context.update({'title': title})
        return context


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        title = 'удаление категории'
        context.update({'title': title})
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        return Product.objects.filter(category__id=self.kwargs['pk']).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Товары'
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context.update({'title': title, 'category': category})
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        title = 'Создание товара'
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context.update({'title': title, 'category': category})
        return context

    def get_success_url(self):
        category_id = self.kwargs['pk']
        return reverse_lazy('admin_staff:products', kwargs={'pk': category_id})


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        title = 'Редактирование товара'
        category = get_object_or_404(Product, pk=self.kwargs['pk']).category
        context.update({'title': title, 'category': category})
        return context

    def get_success_url(self):
        category_id = self.kwargs['pk']
        return reverse_lazy('admin_staff:products', kwargs={'pk': category_id})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    context_object_name = 'product_to_del'

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        title = 'удаление товара'
        context.update({'title': title})
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        product_pk = self.kwargs['pk']
        category_pk = get_object_or_404(Product, pk=product_pk).category.pk
        return reverse_lazy('admin_staff:products', kwargs={'pk': category_pk})
