from .models import Category, Product
from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ReviewForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    return render(request,
         'shop/product/list.html',
         {'category': category,
         'categories': categories,
         'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    # Получение всех отзывов для текущего продукта
    reviews = product.reviews.all()

    # Обработка формы для добавления отзыва
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Пользователь, оставивший отзыв
            review.save()
            return redirect('shop:product_detail', id=product.id, slug=product.slug)
    else:
        form = ReviewForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'reviews': reviews,  # Передача отзывов в шаблон
                   'form': form})        # Передача формы для добавления отзыва
