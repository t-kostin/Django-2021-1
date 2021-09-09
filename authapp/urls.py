from django.urls import path
from .views import register, edit, verify, UserLoginView, UserLogoutView
# from .views import login, logout

app_name = 'authapp'
urlpatterns = [
    # path('login/', login, name='login'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', logout, name='logout'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
