from django.shortcuts import render, get_object_or_404, redirect
from .models import Catagory, Product
from cart.forms import CarAddProductForm


def product_list(request, catagory_slug=None):
    # print('Hi')
    language = request.LANGUAGE_CODE
    print(language)
    # catagory = get_object_or_404(Catagory,
    #                              translations__language_code=language,
    #                              translations__slug=catagory_slug)
    catagory = None
    catagories = Catagory.objects.all()
    products = Product.objects.filter(available=True)
    if catagory_slug:
        catagory = get_object_or_404(
            Catagory, translations__slug=catagory_slug)
        products = products.filter(catagory=catagory)

    return render(request, 'shop/product/list.html',
                  {'catagory': catagory,
                   'catagories': catagories,
                   'products': products})


def product_details(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CarAddProductForm()
    return render(request,
                  'shop/product/details.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
