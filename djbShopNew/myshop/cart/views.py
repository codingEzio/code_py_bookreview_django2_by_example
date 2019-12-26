from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart as SessionCart

from shop.models import Product
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


__doc__ = """Notes:
  Any functions that don't have a `render` function or a template file name
  must be called via other apps' views or even templates(views actually XD).

  For example,
    cart_detail     simply displaying the cart page (based on 'base.html' ofc)
    cart_remove     being used inside the cart page (eh)
    cart_add        being called to process the form & do sth based on the data

  Also, for the dict part,
    we often use `KEY[VAL]` to assign/change values, in the template
    we kinda always use dot notation (e.g. VAR.update_quantity_form.quantity)
"""


def cart_detail(request):
    """
    Notes on the "coupons":
      In the first time we visit view 'cart_detail' (=> cart/detail.html),
      it's not that special.

      But when we click the 'Apply' on the form, it "finds" the ID as an
      model instance then "redirect" us to this view again, but now we
      HAVE a `coupon_id` for `cart_session` (cart/cart.py) to process/calc.

      After the `coupon_apply`, the `coupon_id` was stored in the session,
      which can also be accessed by our 'session' (cart/cart.py : Cart).

      The (2nd time being invoked) 'cart_session' was initializaed with
      all the calculated result based on the `coupon_id` (e.g. discount).

      Right now, we CAN pass the calculated stuff to the 'cart/detail.html',
      of course, after finished "this part" (displaying cart detail), the
      "calculated result" (of instance 'cart_session') still exists, so we
      can still do something about it (all we need is an init to calc res).

      One more thing about "session_cart",
        part of the job was being done in the `Cart` (& initialization)
        part of the job was simply "storing the key in the browser's session"

        Actual process
        1. get the data (from browers' session)
        2. process(while being initialized) based on all the data we got
    """

    # Calc all the results we need when being initialized
    cart_session = SessionCart(request)

    # We actually have used this form before
    #   shop/product/detail.html    simply "add to cart"
    #   cart/detail.html            used for 'update" existing quantities
    for cart_inst in cart_session:
        cart_inst["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": cart_inst["quantity"], "update": True}
        )
    coupon_apply_form = CouponApplyForm()

    return render(
        request=request,
        template_name="cart/detail.html",
        context={
            "cart_session": cart_session,
            "coupon_apply_form": coupon_apply_form,
        },
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
