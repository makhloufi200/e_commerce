from django.urls import path
from cart.views import add_to_cart, remove_from_cart, CartView,decreaseCart,datail_item
from app import views as app_view

app_name = 'mainapp'

urlpatterns = [
	path('', app_view.all_items, name='all_items'),
    path('cart/', CartView, name='cart-home'),
	path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
	path('cart/<slug>', add_to_cart, name='cart'),
	path('item/<int:item_id>/', datail_item, name='datail_item'),
]