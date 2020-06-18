from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, Order
from app.models import Items
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib import messages

# Create your views here.
@login_required
def add_to_cart(request,slug):
	item = get_object_or_404(Items,slug=slug)
	order_item,created = Cart.objects.get_or_create(item=item,user=request.user)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.orderitems.filter(item__slug=item.slug).exists():
			order_item.quantity +=1
			order_item.save()
			messages.info(request,"This Item Quantity was Updated")
			return redirect("mainapp:all_items")
		else:
			order.orderitems.add(order_item)
			messages.info(request,"This Item was added to your Cart")
			return redirect("mainapp:all_items")
	else:
		order = Order.objects.create(user=request.user)
		order.orderitems.add(order_item)
		messages.info(request,"This Item was added to your Cart")
		return redirect("mainapp:all_items")

@login_required		
def remove_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
        # Checking the cart quantity
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.orderitems.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("mainapp:all_items")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("mainapp:all_items")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("mainapp:all_items")
		
def CartView(request):

    user = request.user

    carts = Cart.objects.filter(user=user, purchased=False)
    orders = Order.objects.filter(user=user, ordered=False)

    if carts.exists():
        if orders.exists():
            order = orders[0]
            return render(request, 'cart/home.html', {"carts": carts, 'order': order})
        else:
            messages.warning(request, "You do not have any item in your Cart")
            return redirect("mainapp:home")
		
    else:
        messages.warning(request, "You do not have any item in your Cart")
        return redirect("mainapp:home")

@login_required
def decreaseCart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} has removed from your cart.")
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
        else:
            messages.info(request, f"{item.name} quantity has updated.")
            return redirect("mainapp:cart-home")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("mainapp:cart-home")		
		
def datail_item(request, item_id):
    object = get_object_or_404(Items, pk=item_id)
    return render(request, 'item_detail.html', {'object': object})		