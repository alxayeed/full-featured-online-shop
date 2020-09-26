from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreationForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # clear the cart from the session
            cart.clear()
            # send the task of sending email to celery
            order_created.delay(order.id)

            # redirect to payment module for handling the payments
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreationForm()
    return render(request, 'orders/order/create.html',
                  {'cart': cart,
                   'form': form})
