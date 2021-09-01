from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, FormView

from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm, ShopUserProfileEditForm
from authapp.models import ShopUser


class UserLoginView(LoginView):
    model = ShopUser
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('index')
    form_class = ShopUserLoginForm

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        title = 'Вход'
        context.update({'title': title})
        return context


# def login(request):
#     title = 'вход'
#     login_form = ShopUserLoginForm(data=request.POST or None)
#     next = request.GET['next'] if 'next' in request.GET.keys() else ''
#     if request.method == 'POST' and login_form.is_valid():
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user and user.is_active:
#             auth.login(request, user)
#             if 'next' in request.POST.keys():
#                 return HttpResponseRedirect(request.POST['next'])
#             else:
#                 return HttpResponseRedirect(reverse('index'))
#
#     context = {
#         'title': title,
#         'form': login_form,
#         'next': next,
#     }
#     return render(request, 'authapp/login.html', context)


class UserLogoutView(LogoutView):
    template_name = 'authapp/logout.html'


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('Mail sent successfully')
            else:
                print('Mail not sent')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', context)


@login_required
def edit(request):
    title = 'профиль'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на сайте {settings.DOMAIN_NAME} ' \
              f'пройдите по ссылке: {settings.DOMAIN_NAME}{verify_link}.'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'Activation key error in {user.username}')
        return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'Activation user error: {err.args}')
        return HttpResponseRedirect(reverse('index'))
