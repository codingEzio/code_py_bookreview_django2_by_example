from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_detial(request):
    cart = Cart(request)

    return render(request=request,
                  template_name='cart/detail.html',
                  context={'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned = form.cleaned_data
        cart.add(product=product,
                 quantity=cleaned['quantity'],
                 initial_update_quantity=cleaned['update'])

    return redirect(to='cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect(to='cart:cart_detail')
