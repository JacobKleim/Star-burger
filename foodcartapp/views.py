from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

import phonenumbers

from .models import Product, Order, OrderItem


def is_valid_phonenumber(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):

    data = request.data
    print(request.data)

    if 'products' not in data:
        return Response({'error':
                         'products: Обязательное поле'},
                        status=status.HTTP_400_BAD_REQUEST)
    if data['products'] is None:
        return Response({'error':
                         'products: Это поле не может быть пустым'},
                        status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(data['products'], list):
        return Response({'error':
                         'products: Ожидался list со значениями, но был получен str'},
                        status=status.HTTP_400_BAD_REQUEST)
    if data['products'] == []:
        return Response({'error':
                         'products: Этот список не может быть пустым'},
                        status=status.HTTP_400_BAD_REQUEST)
    for item_data in data['products']:
        order_item_id = item_data['product']
        if not Product.objects.filter(pk=order_item_id).exists():
            return Response({'error': 'products: Недопустимый первичный ключ'},
                            status=status.HTTP_400_BAD_REQUEST)
    required_keys = ['firstname', 'lastname', 'phonenumber', 'address']
    for key in required_keys:
        if key not in data:
            return Response({'error': f'{key}: Обязательное поле'},
                            status=status.HTTP_400_BAD_REQUEST)
    for key, value in data.items():
        if value is None or value == '' or value == []:
            return Response({'error': f'{key}: Некорректное значение'},
                            status=status.HTTP_400_BAD_REQUEST)
    if 'phonenumber' in data and not is_valid_phonenumber(data['phonenumber']):
        return Response({'error': 'phonenumber: Введен некорректный номер телефона'},
                        status=status.HTTP_400_BAD_REQUEST)    

    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        phone=data['phonenumber'],
        address=data['address'],
    )

    order_items = [
        OrderItem(
            order=order,
            product_id=item['product'],
            quantity=item['quantity']
        )
        for item in data['products']
    ]
    OrderItem.objects.bulk_create(order_items)

    return JsonResponse({})
