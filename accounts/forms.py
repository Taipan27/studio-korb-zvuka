"""Формы для приложения accounts."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя (исполнителя/клиента)."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input',
                                       'placeholder': 'example@mail.ru'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-input',
                                      'placeholder': 'Иван'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input',
                                               'placeholder': 'логин'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input',
                                                     'placeholder': '••••••'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input',
                                                     'placeholder': '••••••'})
        self.fields['username'].label = 'Логин'
        self.fields['email'].label = 'Электронная почта'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'


class LoginForm(AuthenticationForm):
    """Форма авторизации."""
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input',
                                      'placeholder': 'логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input',
                                          'placeholder': '••••••'})
    )
