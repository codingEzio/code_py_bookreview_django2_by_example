from decimal import Decimal
from django.conf import settings

from shop.models import Product


class Cart(object):
    """
    Overview of currently implemented methods
    * __init__          cart from session
    * __iter__          make the inst of 'Cart' "loopable"
    * __len__           quantity of products in the cart
    * add               add the product into the cart (quan: 0/1/n++)
    * remove            remove the product from the cart
    * save              mark the session as "modified" before saving
    * get_total_price   the total price for the cart
    """
    def __init__(self, request):
        """
        If there's something in the session, grab it
        if there's nothing   in the session, initialize a empty cart

        All of our session vals will be stored under the key 'CART_SESSION_ID',
        you can just consider it as a dict (init {}, set a[b]=val, del, clear).
        """

        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, initial_update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product.id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if initial_update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the prod from the DB.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for prod in products:
            cart[str(prod.id)]['product'] = prod

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values())
