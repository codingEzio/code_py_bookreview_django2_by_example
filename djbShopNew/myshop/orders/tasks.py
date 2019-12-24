from celery import task
from django.core.mail import send_mail

from .models import Order


__doc__ = """When to use asynchronous tasks?
  - Time-consuming processes, like loading images, converting videos
  - Processes that are subject to failure
    - might not take much time BUT might fail
    - failures like connection failures (how about a retry policy?)
"""


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order_dbobj = Order.objects.get(id=order_id)
    subject = f"Order nr. {order_dbobj.id}"
    message = (
        f"Dear {order_dbobj.first_name},\n\n"
        f"You have successfully placed an order."
        f"Your order id is {order_dbobj.id}."
    )

    mail_sent = send_mail(
        subject=subject,
        message=message,
        from_email="a@a.com",
        recipient_list=[order_dbobj.email],
    )

    return mail_sent
