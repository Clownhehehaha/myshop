from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'email': 'Электронная почта',
            'address': 'Адрес',
            'postal_code': 'Индекс',
            'city': 'Город',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя из аргументов
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            # Заполняем поля из данных пользователя
            self.fields['first_name'].initial = user.first_name
            self.fields['first_name'].widget.attrs['readonly'] = True  # Делаем поле только для чтения

            self.fields['last_name'].initial = user.last_name
            self.fields['last_name'].widget.attrs['readonly'] = True  # Делаем поле только для чтения

            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True
