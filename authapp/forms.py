from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.core.exceptions import ValidationError
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('Только 18+')
        return age


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )
        field_classes = {"username": UsernameField}

    def clean_age(self):
        data = self.cleaned_data.get("age")
        if data < 10 or data > 100:
            raise ValidationError("Please, enter a valid age!")
        return data
