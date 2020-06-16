from django.urls import path

from cart import views as cart_view

app_name = 'cartapp'

urlpatterns = [
	path('cart/<slug>', cart_view.add_to_cart, name='add_to_cart'),
    path('remove/<slug>', cart_view.remove_from_cart, name='remove-cart'),

]