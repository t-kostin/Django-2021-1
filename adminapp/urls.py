from django.urls import path
from adminapp.views import (
    users,
    user_create,
    user_update,
    user_delete,
    categories,
    category_create,
    category_update,
    category_delete,
    products,
    product_create,
    product_read,
    product_update,
    product_delete,
)

app_name = 'adminapp'
urlpatterns = [
    path('users/create/', user_create, name='user_create'),
    path('users/read/', users, name='users'),
    path('users/update/<int:pk>/', user_update, name='user_update'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),

    path('categories/read/', categories, name='categories'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/update/<int:pk>/', category_update, name='category_update'),
    path('categories/delete/<int:pk>/', category_delete, name='category_delete'),

    path('products/read/category/<int:pk>/', products, name='products'),
    # path('products/create/category/<int:pk>/', product_create, name='product_create'),
    # path('products/read/<int:pk>/', product_read, name='product_read'),
    # path('products/update/<int:pk>/', product_update, name='product_update'),
    # path('products/delete/<int:pk>/', product_delete, name='product_delete'),
]
