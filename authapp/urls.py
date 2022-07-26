from authapp.apps import AuthappConfig
from django.urls import path
from authapp.views import MyLoginView, RegisterView, MyLogoutView, EditView

app_name = AuthappConfig.name

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('edit/', EditView.as_view(), name='edit'),
]