from .cart import Cart


def cart(request):
    '''
    Adds the instance of the Cart into the context processor as cart
    '''
    return {'cart': Cart(request)}
