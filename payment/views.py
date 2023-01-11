from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from payment.models import *
from account.models import *
from django.contrib import messages

@login_required(login_url='account:signin')
def checkout(request):
    shipping = ShippingAddress.objects.filter(user=request.user.id)
    if not shipping:
        messages.error(request, 'Please update shipping details to checkout!')
        return redirect('account:profile')

    return render(request, 'payment/checkout.html', context={'title': 'Checkout'})

@login_required(login_url='account:signin')
def complete_order(request):
    if request.POST.get('action') == 'post':
        shipping = ShippingAddress.objects.get(user=request.user.id)

        order = Order.objects.create(
            user = request.user,
            full_name = shipping.full_name,
            email = request.user.email,
            shipping_address = shipping.get_full_address(),
            amount_total = request.session['total'],
        )

        for item in request.session['cart']:
            order_item = OrderItem.objects.create(
                user = request.user,
                order = order,
                product = Product.objects.get(id=item),
                quantity = request.session['cart'][item]['qty'],
                price = request.session['cart'][item]['price'],
            )

        messages.success(request, f'Order #{order.id} placed successfully')
        user_cart = UserCart.objects.filter(username=request.user.username).update(user_cart={}, total=0.0)
        request.session['cart'] = {}
        request.session['total'] = 0.0
        return redirect('payment:my_orders')

    return redirect('payment:checkout')

@login_required(login_url='account:signin')
def my_orders(request):
    orders = Order.objects.filter(user=request.user)

    if len(orders) == 0:
        return render(request, 'empty_cart.html', context={'title': 'My Orders'})
    
    order_items = OrderItem.objects.filter(order__in=orders)
    return render(request, 'payment/my_orders.html', context={'title': 'My Orders', 'orders': orders, 'order_items': order_items})