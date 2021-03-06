from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

import weasyprint

from cart.cart import Cart as SessionCart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created as task_order_created


def order_create(request):
    cart_session = SessionCart(request)

    order_create_form = OrderCreateForm(request.POST)
    if order_create_form.is_valid():
        # The 'Order' part
        order_table_inst = order_create_form.save(commit=False)
        if cart_session.coupon:
            order_table_inst.coupon = cart_session.coupon  # fk VS class attr
            order_table_inst.discount = cart_session.coupon.discount
        order_table_inst.save()

        # The 'OrderItem' part
        for cart_inst in cart_session:
            OrderItem.objects.create(
                order=order_table_inst,
                product=cart_inst["product"],
                price=cart_inst["price"],
                quantity=cart_inst["quantity"],
            )

        cart_session.clear()
        task_order_created.delay(order_table_inst.id)

        return render(
            request=request,
            template_name="orders/order/created.html",
            context={"order_table_inst": order_table_inst},
        )
    else:
        order_create_form = OrderCreateForm()

    return render(
        request=request,
        template_name="orders/order/create.html",
        context={
            "cart_session": cart_session,
            "order_create_form": order_create_form,
        },
    )


@staff_member_required
def admin_order_detail(request, order_id):
    order_table_inst = get_object_or_404(Order, id=order_id)
    return render(
        request=request,
        template_name="admin/orders/order/detail.html",
        context={"order_table_inst": order_table_inst},
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    order_table_inst = get_object_or_404(Order, id=order_id)
    html = render_to_string(
        template_name="orders/order/pdf.html",
        context={"order_table_inst": order_table_inst},
    )

    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f"filename=order_{order_table_inst.id}.pdf"

    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(settings.STATICFILES_DIRS[0] + "css/pdf.css")
        ],
    )

    return response
