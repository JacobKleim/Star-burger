from django.http import JsonResponse
from django.templatetags.static import static
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, DecimalField

from .models import Product, Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(
        many=True, allow_empty=False, write_only=True)
    # total_price = DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['firstname',
                  'lastname',
                  'phonenumber',
                  'address',
                  'products']
        
    # def get_total_price(self, obj):
    #     return obj.total_price  


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

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    print(serializer.validated_data)
    try:
        with transaction.atomic():
            order = Order.objects.create(
                firstname=serializer.validated_data['firstname'],
                lastname=serializer.validated_data['lastname'],
                phonenumber=serializer.validated_data['phonenumber'],
                address=serializer.validated_data['address'],
            )

            order_items = [
                OrderItem(
                    order=order,
                    product_id=item['product'].id,
                    quantity=item['quantity']
                )
                for item in serializer.validated_data['products']
            ]
            OrderItem.objects.bulk_create(order_items)

    except Exception as e:
        return Response(
            {'error': 'Ошибка при создании заказа.'
             f'{e}'},
            status=status.HTTP_400_BAD_REQUEST
            )

    return Response(
        serializer.data, status=status.HTTP_201_CREATED
    )
