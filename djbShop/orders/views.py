from django.shortcuts import render

from cart.cart import Cart

from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()

            # async tasks powered by celery yo!
            order_created.delay(order_id=order.id)

            return render(request=request,
                          template_name='orders/order/created.html',
                          context={'order': order})
    else:
        form = OrderCreateForm()

    return render(request=request,
                  template_name='orders/order/create.html',
                  context={
                      'cart': cart,
                      'form': form
                  })
