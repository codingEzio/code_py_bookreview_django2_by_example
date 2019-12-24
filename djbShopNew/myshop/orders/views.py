from django.shortcuts import render

from cart.cart import Cart as SessionCart
from .models import Order, OrderItem
from .forms import OrderCreateForm


def order_create(request):
    cart_session = SessionCart(request)

    form = OrderCreateForm(request.POST)
    if form.is_valid():
        # The 'Order' part
        order_table_inst = form.save()

        # The 'OrderItem' part
        for cart_inst in cart_session:
            OrderItem.objects.create(
                order=order_table_inst,
                product=cart_inst["product"],
                price=cart_inst["price"],
                quantity=cart_inst["quantity"],
            )

        cart_session.clear()
        return render(
            request=request,
            template_name="orders/order/created.html",
            context={"order_table_inst": order_table_inst},
        )
    else:
        form = OrderCreateForm()

    return render(
        request=request,
        template_name="orders/order/create.html",
        context={"cart_session": cart_session, "form": form},
    )
