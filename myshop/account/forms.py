from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
     username = forms.CharField()
     password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'email': 'Электронная почта',
        }
        help_texts = {
            'username': 'Обязательное поле. 150 символов или меньше. Можно использовать буквы, цифры и символы @/./+/-/_',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        labels = {
            'date_of_birth': 'Дата рождения',
            'photo': 'Фото профиля',
        }

