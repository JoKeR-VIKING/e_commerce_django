from django.shortcuts import render, get_object_or_404
from store.models import Product
from account.models import UserCart
from .cart import Cart
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)

    if len(cart) > 0:
        return render(request, 'cart/cart_summary.html', context={'title': 'Product Destination | Cart', 'cart': cart})

    return render(request, 'empty_cart.html', context={'title': 'Product Destination | Cart'})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity)

        UserCart.objects.filter(username=request.user.username).update(user_cart=request.session['cart'], total=request.session['total'])

        return JsonResponse({'cart_qty': len(cart)})

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        product = get_object_or_404(Product, id=product_id)
        cart.delete(product)

        UserCart.objects.filter(username=request.user.username).update(user_cart=request.session['cart'], total=request.session['total'])

        return JsonResponse({'cart_qty': len(cart), 'cart_total': cart.total})

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))

        product = get_object_or_404(Product, id=product_id)
        cart.update(product, quantity)

        UserCart.objects.filter(username=request.user.username).update(user_cart=request.session['cart'], total=request.session['total'])

        return JsonResponse({'cart_qty': len(cart), 'cart_total': cart.total})