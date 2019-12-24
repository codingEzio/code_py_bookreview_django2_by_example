from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart as SessionCart
from .forms import CartAddProductForm


__doc__ = """Notes:
  Any functions that don't have a `render` function or a template file name
  must be called via other apps' views or even templates(views actually XD).

  For example,
    cart_detail     simply displaying the cart page (based on 'base.html' ofc)
    cart_remove     being used inside the cart page (eh)
    cart_add        being called to process the form & do sth based on the data
"""


def cart_detail(request):
    cart_session = SessionCart(request)
    return render(
        request=request,
        template_name="cart/detail.html",
        context={"cart_session": cart_session},
    )


@require_POST
def cart_add(request, product_id):
    """
    There actually isn't much weird stuff going on, taking `cleaned["update"]`
    as an example, we couldn't find this anywhere in this page, well, since it
    was related to form, you should check at least these places:
      forms.py       this should be the 1st place you go
      <form> (tmpl)  the 2nd place to see if you still can't find anything
    """

    cart_session = SessionCart(request)
    product = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned = form.cleaned_data

        # These two keys came from the 'forms.py'
        cart_session.add(
            product=product,
            quantity=cleaned["quantity"],
            update_quantity=cleaned["update"],
        )

    return redirect(to="cart:cart_detail")


def cart_remove(request, product_id):
    cart_session = SessionCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart_session.remove(product)
    return redirect(to="cart:cart_detail")
