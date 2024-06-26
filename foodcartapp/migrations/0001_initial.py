import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20, verbose_name='имя')),
                ('lastname', models.CharField(max_length=20, verbose_name='фамилия')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, verbose_name='телефон')),
                ('address', models.CharField(max_length=200, verbose_name='адрес')),
                ('payment', models.CharField(choices=[('Н', 'Наличные'), ('Э', 'Электронно')], db_index=True, default='Н', max_length=2, verbose_name='способ оплаты')),
                ('registered', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='зарегистрирован')),
                ('called', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='позвонили в')),
                ('delivered', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='доставили в')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='комментарий')),
                ('status', models.CharField(choices=[('НО', 'Необработан'), ('ПР', 'Передан ресторану'), ('Г', 'Готовится'), ('Пк', 'Передан курьеру'), ('В', 'Выполнен')], db_index=True, default='НО', max_length=2, verbose_name='статус')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='адрес')),
                ('contact_phone', models.CharField(blank=True, max_length=50, verbose_name='контактный телефон')),
            ],
            options={
                'verbose_name': 'ресторан',
                'verbose_name_plural': 'рестораны',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена')),
                ('image', models.ImageField(upload_to='', verbose_name='картинка')),
                ('special_status', models.BooleanField(db_index=True, default=False, verbose_name='спец.предложение')),
                ('description', models.TextField(blank=True, max_length=200, verbose_name='описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='foodcartapp.productcategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена продукта на момент заказа')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='foodcartapp.order', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodcartapp.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'товар в заказе',
                'verbose_name_plural': 'товары в заказе',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodcartapp.restaurant', verbose_name='ресторан'),
        ),
        migrations.CreateModel(
            name='RestaurantMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.BooleanField(db_index=True, default=True, verbose_name='в продаже')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='foodcartapp.product', verbose_name='продукт')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='foodcartapp.restaurant', verbose_name='ресторан')),
            ],
            options={
                'verbose_name': 'пункт меню ресторана',
                'verbose_name_plural': 'пункты меню ресторана',
                'unique_together': {('restaurant', 'product')},
            },
        ),
    ]
