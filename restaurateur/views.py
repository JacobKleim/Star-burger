import requests
from django.conf import settings
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from geopy import distance

from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem

from geolocation.models import Location


def fetch_coordinates(apikey, address): 
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    
    return lon, lat


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items', 'category'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def get_available_restaurants(order):
    order_items = order.items.all()
    for item in order_items:
        product_availability = RestaurantMenuItem.objects.filter(
            product=item.product, availability=True
            ).select_related('restaurant', 'product')
        restaurants_with_product = set(
            [item.restaurant for item in product_availability])
    return restaurants_with_product


def get_coordinates(addresses, api_key):
    locations = Location.objects.filter(address__in=addresses)
    coordinates = {loc.address: (loc.latitude, loc.longitude) for loc in locations}

    missing_addresses = set(addresses) - set(coordinates.keys())
    for address in missing_addresses:
        lon, lat = fetch_coordinates(api_key, address)
        coordinates[address] = (lon, lat)
        Location.objects.create(address=address, latitude=lat, longitude=lon)

    return coordinates


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_items = Order.objects.with_total_price().exclude(
        status='В'
        ).prefetch_related('items__product').order_by('-status')
    addresses = {order.address for order in order_items}
    for order in order_items:
        available_restaurants = get_available_restaurants(order)
        addresses.update(
            restaurant.address for restaurant in available_restaurants)

    coordinates = get_coordinates(addresses, settings.YANDEX_GEOCODER_API_KEY)

    for order in order_items:
        order.available_restaurants = get_available_restaurants(order)
        order_coordinates = coordinates.get(order.address)
        for restaurant in order.available_restaurants:
            restaurant_coordinates = coordinates.get(restaurant.address)
            if order_coordinates and restaurant_coordinates:
                restaurant.distance_to_order = distance.distance(
                    order_coordinates, restaurant_coordinates).km
            else:
                restaurant.distance_to_order = None
        order.available_restaurants = sorted(
            order.available_restaurants,
            key=lambda r: r.distance_to_order
        )
    return render(request, template_name='order_items.html', context={
        'order_items': order_items
    })
