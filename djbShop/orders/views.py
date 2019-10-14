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

            # If I send the mail synchorously, everything is fine (since it
            # doesn't have relations with Celery|RabbitMQ).
            # But when I added the `.delay`, it stopped working, specifically,
            # the 'tasks.py', i.e. this doesn't work: Order.objects.get(id=order_id),
            # an error was raised called 'relation "orders_order" does not exist' (ah)
            order_created(order_id=order.id)

            # In short, the current status is:
            #   async-send email    NOT WORKING
            #   sync-send email     WORKING (if I removed the '.delay')
            #   creating orders     WORKING

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
