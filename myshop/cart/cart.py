from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавить товар в корзину либо обновить его количество.
        """
        product_id = str(product.id)

        # Если товар еще не добавлен в корзину, создаем запись о нем.
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        # Если override_quantity True, то заменяем количество товара на выбранное.
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            # Если override_quantity False, то заменяем количество на новое, а не прибавляем.
            self.cart[product_id]['quantity'] = quantity

        # Сохраняем изменения в корзине.
        self.save()

    def save(self):
        """
        Пометить сеанс как "измененный", чтобы сохранить изменения.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Удалить товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        product_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()  # Сделать копию корзины, чтобы не изменять её в процессе
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])  # Преобразуем цену в Decimal
            item['total_price'] = item['price'] * item['quantity']  # Вычисляем итоговую цену
            yield item  # Возвращаем товар по очереди

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Вычислить общую стоимость корзины.
        """
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        """
        Очистить корзину из сессии.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()


