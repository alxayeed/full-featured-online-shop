from celery import task
from django.core.mail import send_mail()
from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order number {order.id}'
    message = f'Dear {order.first_name}\n\n'\
        f'Your order has been sucessfully placed\n' \
        f'Your order number is {order.id}'
    mail_sent = send_mail(subject,
                          message,
                          '16103213@iubat.edu',
                          [order.email])

    return mail_sent
