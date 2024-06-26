from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.timezone import make_naive
from .forms import *
from .models import *
from datetime import datetime, timedelta
import random
import re
import requests
import json

def format_phone_number(number):
    """Проверяет корректность введенного номера телефона."""

    # Удаление всех нецифровых символов
    cleaned_text = re.sub(r'\D', '', number)

    # Проверка, что осталось ровно 10 цифр
    if len(cleaned_text) == 10:
        return True
    else:
        return False


def generate_code():
    """Генерирует случайный четырехзначный код."""
    return random.randint(1000, 9999)


def send_sms(phone_number, message):
    """Отправляет SMS с кодом на указанный номер телефона.
    
    Здесь должен быть код для интеграции с вашим сервисом отправки SMS.
    """

    # URL сервиса для отправки SMS
    url = "https://direct.i-dgtl.ru/api/v1/message"

    #Заголовки запроса
    headers = {
        'Authorization': 'Basic NzkyOTpzeFlTUGd2c0VMOTZtME8xdndLVkVv',
        # 'Authorization': 'Basic NzkyNzpySFpCNmNsWW5hakxFSnczVFk0S3I4',
        'Content-Type': 'application/json'
    }

    # Параметры запроса
    data = [
        {
            "channelType": "SMS",
            "senderName": "sms_promo",
            "destination": f'7{phone_number}',
            "content": message
        }
    ]

    # Отправка запроса
    response = requests.post(url, headers=headers, data=json.dumps(data))

# Обработка ответа
    if response.status_code == 200:
        print("Сообщение успешно отправлено")
        print(response.text)
    else:
        print(f"Ошибка при отправке сообщения: {response.status_code}")
        print(response.text)

    print(f'Nubmer: +7{phone_number}')
    print(f'Code: {message}')
    return


def login_request(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            code = form.cleaned_data['code']

            try:
                verification = PhoneVerification.objects.get(phone_number=phone_number)
            except PhoneVerification.DoesNotExist:
                user = User.objects.create_user(username=phone_number)
                verification = PhoneVerification(user=user, phone_number=phone_number, verified=False)
                verification.verification_code = str(generate_code())
                verification.save()

                # Проверка времени последнего запроса
                if verification.last_request_time:
                    last_request_naive = make_naive(verification.last_request_time)
                    if datetime.now() - last_request_naive < timedelta(minutes=2):
                        messages.error(request, "Вы можете запрашивать SMS не чаще одного раза в 2 минуты.")
                        return render(request, 'main/login.html', {'form': form})

                verification.last_request_time = datetime.now()
                verification.save()

                send_sms(phone_number, f'Код авторизации Суши-Ок {verification.verification_code}')
                return render(request, 'main/code.html', {'form': form, 'phone_number': phone_number})

            if not code:
                # Проверка времени последнего запроса
                if verification.last_request_time:
                    last_request_naive = make_naive(verification.last_request_time)
                    if datetime.now() - last_request_naive < timedelta(minutes=2):
                        messages.error(request, "Вы можете запрашивать SMS не чаще одного раза в 2 минуты.")
                        return render(request, 'main/code.html', {'form': form, 'phone_number': phone_number})

                verification.verification_code = str(generate_code())
                verification.last_request_time = datetime.now()
                verification.save()

                send_sms(phone_number, f'Код авторизации Суши-Ок {verification.verification_code}')
                return render(request, 'main/code.html', {'form': form, 'phone_number': phone_number})

            if code and verification.verification_code == code:
                verification.verified = True
                verification.save()
                login(request, verification.user)
                return redirect('index')
            else:
                form.add_error('code', 'Invalid verification code')
                messages.error(request, 'Введен неверный код')
                return redirect('login')
        else:
            messages.error(request, 'Номер телефона введен неверно')
            return render(request, 'main/login.html', {'form': form})
    else:
        return render(request, 'main/login.html', {'form': form})


@login_required
def logout_request(request):
    logout(request)
    return redirect('index')


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    new = Product.objects.filter(new=1)
    context = {
        'products':products,
        'categories':categories,
        'new':new,
    }
    return render(request, 'main/index.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'main/category.html', context)

@login_required
def checkout(request):

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, sended=False)
        items = order.orderitem_set.all()
        totalItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        totalItems = order['get_cart_items']

    user = request.user
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Предполагаем, что у нас есть некий экземпляр Order
            # В реальном приложении здесь может быть логика для получения или создания Order
            order = Order.objects.get(user=user)  # Пример получения первого заказа

            # Создание экземпляра ShippingAddress с данными из формы
            address = ShippingAddress(
                order=order,
                address=form.cleaned_data['address'],
                orderType=form.cleaned_data['orderType'],
                paymentType=form.cleaned_data['paymentType']
            )
            address.save()  # Сохраняем объект в базу данных
            
            return redirect('complete')  # Редирект на страницу успеха или другую страницу
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'items':items, 
        'order':order, 
        'totalItems':totalItems
    }

    return render(request, 'main/checkout.html', context)


@login_required
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, sended=False)
        items = order.orderitem_set.all()
        totalItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        totalItems = order['get_cart_items']

    context = {
        'items':items, 
        'order':order, 
        'totalItems':totalItems
    }
    return render(request, 'main/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId)
    print(action)

    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user, sended=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def updateCheckout(request):
    data = json.loads(request.body)
    orderType = data['orderType']
    paymentType = data['paymentType']
    address = data['address']
    user = request.user
    order = Order.objects.get(user=user, sended=False)
    items = order.orderitem_set.all()
    totalItems = order.get_cart_total

    shipping, created = ShippingAddress.objects.get_or_create(order=order)
    shipping.address = address
    shipping.orderType = orderType
    shipping.paymentType = paymentType
    shipping.save()

    order.sended = True
    order.save()

    orderTypeStr = ''
    if orderType == 'car':
        orderTypeStr = 'Доставка'
    else:
        orderTypeStr = 'Самовывоз'

    paymentTypeStr = ''
    if paymentType == 'cash':
        paymentTypeStr = 'Наличные'
    else:
        paymentTypeStr = 'Карта'

    text = f'Заказ #{order.order_id}\n\nТип: {orderTypeStr} | Оплата: {paymentTypeStr}\n\nАдрес: {address}\n\nТелефон: +7{user.username}\n\nСостав заказа:\n'

    items = OrderItem.objects.filter(order=order)
    for i in items:
        print(i.product, i.quantity)
        text += f"{i.quantity} - {i.product}\n"
    
    text += f"\n\nСумма заказа - {totalItems}"

    print(text)

    # URL API
    url = "https://api.puzzlebot.top/"

    # Параметры запроса
    params = {
        'token': '0O61PQUHwCHgK2INgiBjuH7AphSk6PLB',
        'method': 'postSend'
    }

    data = {
        "chats_ids": "private",
        "text": text,
        "type": "message"
    }

    # Отправка POST-запроса
    response = requests.post(url, params=params, json=data)

    # Проверка ответа
    if response.status_code == 200:
        print("Запрос успешно выполнен!")
        print("Ответ сервера:", response.json())
    else:
        print("Ошибка в запросе:", response.status_code)

    return JsonResponse('Order was added', safe=False)


def complete(request):
    context = {}
    return render(request, 'main/complete.html', context)


def statistics(request):
    
    if request.user.is_superuser:
        # Агрегируем данные, суммируя quantity по каждому product
        products = OrderItem.objects.select_related('product').values('product__name').annotate(total_quantity=Sum('quantity')).order_by()

        context = {
            'products':products
        }
        return render(request, 'main/stat.html', context)

    return redirect('index')