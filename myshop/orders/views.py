from django.urls import reverse
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    cart = Cart(request)

    # Если форма была отправлена (POST-запрос)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, user=request.user)  # Передаем текущего пользователя в форму
        if form.is_valid():
            # Сохраняем заказ, но не коммитим сразу
            order = form.save(commit=False)
            order.user = request.user  # Привязка заказа к текущему авторизованному пользователю
            order.save()

            # Создаем объекты OrderItem для каждого товара в корзине
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Очистить корзину после оформления заказа
            cart.clear()

            # Отправить заказ в фоновые задачи (например, для обработки/уведомлений)
            order_created.delay(order.id)

            # Сохранить id заказа в сессии
            request.session['order_id'] = order.id

            # Перенаправление на страницу платежа
            return redirect(reverse('payment:process'))

    else:
        # Инициализация пустой формы
        form = OrderCreateForm(user=request.user)  # Передаем пользователя для заполнения данных

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
