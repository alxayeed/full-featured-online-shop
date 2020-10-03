from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupon.models import Coupon


class Cart(object):

    def __init__(self, request):
        """
        This method will initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store coupon_id from session
        # print(self.session.get('coupon_id'))
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=0, override_quantity=False):
        '''
        Add a product into the cart
        '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        '''
        This method marks this session as 'modified' , then django will save the cart in the session
        this tells Django that session has changed, and needs to be save
        '''
        self.session.modified = True

    def remove(self, product):
        '''
        remove a product from the cart
        '''
        product_id = str(product.id)
        if product_id in cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''
        Iterate over each item in the cart, and get the related product from the database
        '''
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        '''
        count all items in the cart
        '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''
        calculates total price of the cart
        '''
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        '''
        this will remove the cart from the session
        '''
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # coupon methods

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)

            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
