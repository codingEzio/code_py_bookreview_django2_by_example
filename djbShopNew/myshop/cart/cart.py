from django.conf import settings


class Cart(object):
    """
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
