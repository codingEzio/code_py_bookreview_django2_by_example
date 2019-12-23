from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    """
    This whole class works around/with things related to session|request.

    Why use session?
      Because HTTP is stateless, in order to associate a request to any
      other request, you need a way to store user data between requests.
    """

    def __init__(self, request):
        """
        Initialize the cart
          if there is one, read it
          if there isn't , create a blank {}
        """
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # Mark the session as "modified" to make sure it gets saved
        #   https://docs.djangoproject.com/en/3.0/topics/http/sessions/#when-sessions-are-saved
        self.session.modified = True
