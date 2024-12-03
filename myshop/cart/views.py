from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
     cart = Cart(request)
     product = get_object_or_404(Product, id=product_id)
     form = CartAddProductForm(request.POST)
     if form.is_valid():
         cd = form.cleaned_data
         cart.add(product=product,
                  quantity=cd['quantity'],
                  override_quantity=cd['override'])
     return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
     cart = Cart(request)
     product = get_object_or_404(Product, id=product_id)
     cart.remove(product)
     return redirect('cart:cart_detail')



def cart_detail(request):
    cart = Cart(request)
    quantity_choices = range(1, 11)  # Список от 1 до 10
    return render(request, 'cart/detail.html', {'cart': cart, 'quantity_choices': quantity_choices})


def cart_update(request, product_id):
    cart = Cart(request)
    quantity = request.POST.get('quantity')  # Получаем количество товара из формы

    # Преобразуем в целое число (если значение не пустое)
    if quantity:
        try:
            quantity = int(quantity)  # Преобразуем строку в целое число
        except ValueError:
            # Если значение нельзя преобразовать в int, возвращаем ошибку
            pass

    # Обновляем корзину
    try:
        product = Product.objects.get(id=product_id)
        cart.add(product=product, quantity=quantity)  # Обновляем корзину с новым количеством
    except Product.DoesNotExist:
        pass

    return redirect('cart:cart_detail')  # Перенаправляем обратно в корзину
