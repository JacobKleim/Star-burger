from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from django.db.models import Sum, F


PAYMENT_CHOICES = [
        ('Н', 'Наличные'),
        ('Э', 'Электронно'),
    ]

STATUS_CHOICES = [
        ('НО', 'Необработан'),
        ('ПР', 'Передан ресторану'),
        ('Г', 'Готовится'),
        ('Пк', 'Передан курьеру'),
        ('В', 'Выполнен'),
    ]


class OrderQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(
            total_price=Sum(
                F('items__product_price') * F('items__quantity')
                )
        )


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class Order(models.Model):
    firstname = models.CharField(verbose_name='имя', max_length=20)
    lastname = models.CharField(verbose_name='фамилия', max_length=20)
    phonenumber = PhoneNumberField(verbose_name='телефон', db_index=True)
    address = models.CharField(verbose_name='адрес', max_length=200)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ресторан'
    )
    payment = models.CharField(
        max_length=2,
        choices=PAYMENT_CHOICES,
        default='Н',
        verbose_name='способ оплаты',
        db_index=True
    )
    registered = models.DateTimeField(
        verbose_name='зарегистрирован',
        db_index=True,
        auto_now_add=True)
    called = models.DateTimeField(
        verbose_name='позвонили в',
        blank=True,
        null=True,
        db_index=True)
    delivered = models.DateTimeField(
        verbose_name='доставили в',
        blank=True,
        null=True,
        db_index=True)
    comment = models.CharField(
        verbose_name='комментарий',
        max_length=200,
        blank=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='НО',
        verbose_name='статус',
        db_index=True
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.phonenumber}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='заказ')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='продукт')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество')
    product_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='цена продукта на момент заказа',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказе'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
