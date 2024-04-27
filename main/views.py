from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *

def index(request):
    return render(request, 'main/index.html')

def catalog(request):
    categories = Category.objects.all()  # Получаем список всех категорий
    products = Product.objects.all()

    # Получение параметра сортировки из GET-запроса
    sort_by = request.GET.get('sort_by')

    # Сортировка товаров в зависимости от параметра сортировки
    if sort_by == 'newest':
        products = products.order_by('-production_year')
    elif sort_by == 'oldest':
        products = products.order_by('production_year')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'price-':
        products = products.order_by('-price')
    elif sort_by == 'price+':
        products = products.order_by('price')

    # Здесь должен быть код для отображения страницы с товарами,
    # с учетом сортировки
    return render(request, 'main/catalog/catalog.html', {'categories': categories, 'products': products})

def category(request, cat_id):
    cats = Category.objects.all()
    category = Category.objects.get(pk=cat_id)
    products = Product.objects.filter(category=category)

    # Получение параметра сортировки из GET-запроса
    sort_by = request.GET.get('sort_by')

    # Сортировка товаров в зависимости от параметра сортировки
    if sort_by == 'newest':
        products = products.order_by('-production_year')
    elif sort_by == 'oldest':
        products = products.order_by('production_year')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'price-':
        products = products.order_by('-price')
    elif sort_by == 'price+':
        products = products.order_by('price')
    else:
        # Если параметр сортировки не указан или некорректен, выводим товары без сортировки
        pass

    return render(request, 'main/catalog/catalog.html', {'category': category, 'products': products, 'cats': cats})

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'main/product/product.html', {'product': product})

@login_required
def cart(request):
    cart_items = Cart.objects.all()
    total_cost = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'main/cart/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item, created = Cart.objects.get_or_create(client=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect(reverse('cart'))

@login_required
def order(request):
    order_items = Order.objects.filter(user=request.user)
    return render(request, 'main/order/order_menu.html', {'order_items': order_items})

@login_required
def order_add(request, product_id):
    if request.method == 'POST':
        # Получаем товар по его идентификатору
        product = Product.objects.get(pk=product_id)

        # Создаем экземпляр заказа для текущего пользователя и товара
        order = Order.objects.create(
            user=request.user,
            product=product,
            status='New'  # Изменяем на нужный вам статус
        )

        # Удаляем все товары из корзины для текущего пользователя
        Cart.objects.filter(client=request.user).delete()

        # Перенаправляем пользователя на страницу заказов
        return redirect('order')
    else:
        # Если метод запроса не POST, возвращаем пользователя на страницу корзины
        return redirect('cart')


def about(request):
    return render(request, 'main/about.html')

def wherefind(request):
    return render(request, 'main/wherefind.html')
