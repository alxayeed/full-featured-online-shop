from django.shortcuts import render, get_object_or_404, redirect
from .models import Catagory, Product


def product_list(request, catagory_slug=None):
    catagory = None
    catagories = Catagory.objects.all()
    products = Product.objects.filter(available=True)
    if catagory_slug:
        catagory = get_object_or_404(Catagory, slug=catagory_slug)
        products = products.filter(catagory=catagory)

    return render(request, 'shop/product/list.html',
                  {'catagory': catagory,
                   'catagories': catagories,
                   'products': products})


def product_details(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    return render(request,
                  'shop/product/details.html',
                  {'product': product})
