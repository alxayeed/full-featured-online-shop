from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@task
def payment_completed(order_id):
    '''
    asynchronus task to send email to the buyer with pdf invoice
    '''
    order = Order.objects.get(id=order_id)

    # invoice email
    subject = f'Venilla Shop - EE Invoice No. {order.id}'
    message = 'Thanks for purchasing from our shop\n Please find the attached invoice for your purchase details'
    email = EmailMessage(subject,
                         message,
                         '16103213@iubat.edu',
                         [order.email])
    # generate pdf
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)

    # attach pdf with the email
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')

    # send e-mail
    email.send()
