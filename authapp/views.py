from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

import django

django.setup()

from authapp.models import User


class MyLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }


class RegisterView(TemplateView):
    template_name = 'authapp/register.html'
    extra_context = {
        'title': 'Регистрация'
    }

    def post(self, request, *args, **kwargs):
        try:
            if all(
                    (
                            request.POST.get('username'),
                            request.POST.get('email'),
                            request.POST.get('password1'),
                            request.POST.get('password2'),
                            request.POST.get('firstname'),
                            request.POST.get('lastname'),
                            request.POST.get('password1') == request.POST.get('password2')
                    )
            ):
                new_user = User.objects.create(
                    username=request.POST.get('username'),
                    email=request.POST.get('email'),
                    first_name=request.POST.get('firstname'),
                    last_name=request.POST.get('lastname'),
                    age=request.POST.get('age') if request.POST.get('age') else 0,
                    avatar=request.FILES.get('avatar') if request.FILES.get('avatar') else 0,
                )
                new_user.set_password(request.POST.get('password1'))
                new_user.save()
                messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f'Ошибка ввода данных {request.POST.get("username")}')
                return HttpResponseRedirect(reverse('authapp:register'))
        except Exception as e:
            messages.add_message(
                request,
                messages.WARNING,
                f'Ошибка регистрации {e}')
            return HttpResponseRedirect(reverse('authapp:register'))

    class Meta:
        app_label = "authapp"


class MyLogoutView(LogoutView):
    template_name = 'authapp/logout.html'


class EditView(TemplateView):
    template_name = 'authapp/edit.html'
    extra_context = {
        'title': 'Изменение данных'
    }

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.POST.get('username'):
                request.user.username = request.POST.get('username')
            if request.POST.get('first_name'):
                request.user.first_name = request.POST.get('first_name')
            if request.POST.get('last_name'):
                request.user.last_name = request.POST.get('last_name')
            if request.POST.get('age'):
                request.user.age = request.POST.get('age')
            if request.POST.get('email'):
                request.user.email = request.POST.get('email')
            if request.POST.get('password'):
                request.user.set_password(request.POST.get('password'))
        else:
            messages.add_message(
                request,
                messages.WARNING,
                'Необходимо авторизоваться')
        request.user.save()
        return HttpResponseRedirect(reverse('authapp:edit'))
