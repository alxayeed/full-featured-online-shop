from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CarAddProductForm
from coupon.forms import CouponApplyForm


@require_POST
def add_cart(request, product_id):
    '''
    method for adding items to the cart
    '''
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CarAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def remove(request, product_id):
    '''
    method for removing an item from the cart
    '''
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    '''
    method for showing details of the cart
    '''
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CarAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/details.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
