from os import environ

from django.core.mail import send_mail
from celery import shared_task

from .models import Order

MAIL_SENDER = environ.get('EMAIL_HOST_USER')


@shared_task
def order_created(order_id):
    """
    Task to send an email notification when an order is created.
    """

    # current status: relation "orders_order" does not exist
    order = Order.objects.get(id=order_id)

    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name},\nYou have sucessfully placed an order. '
        f'Your order ID is {order.id}')

    mail_sent = send_mail(subject=subject,
                          message=message,
                          from_email=MAIL_SENDER,
                          recipient_list=[order.email])

    return mail_sent
