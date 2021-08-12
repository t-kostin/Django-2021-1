from django.urls import path
from adminapp.views import (
    # users,
    # user_create,
    # user_update,
    # user_delete,
    # categories,
    # category_create,
    # category_update,
    # category_delete,
    # products,
    # product_create,
    # product_read,
    # product_update,
    # product_delete,
    UserListView,
    UserCreateView,
    ProductDetailView,
    UserUpdateView,
    UserDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = 'adminapp'
urlpatterns = [
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/read/', UserListView.as_view(), name='users'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    path('categories/read/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('products/read/category/<int:pk>/', ProductListView.as_view(), name='products'),
    path('products/create/category/<int:pk>/', ProductCreateView.as_view(), name='product_create'),
    path('products/read/<int:pk>/', ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
