from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from authapp.models import User
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm


class MyLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }


class RegisterView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainapp:index')
    # template_name = 'authapp/register.html'


class MyLogoutView(LogoutView):
    template_name = 'authapp/logout.html'


class EditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    # template_name = 'authapp/edit.html'

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('authapp:edit', args=[self.request.user.pk])

