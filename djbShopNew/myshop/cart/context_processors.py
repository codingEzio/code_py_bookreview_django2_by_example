from .cart import Cart


__doc__ = """A brief notes on context processors:
  What is it?
  - You could think it as a global 'return render(.. context={ ?? })' in views

  What can it do?
  - Make something available globally to all templates

  Steps
  1. create a file, return a dict contains stuff you wanna make it globally
  2. add "APP.FILE.METHOD" to settings (TEMPLATES>OPTIONS>context_processors)
  3. use it (in templates of course)

  My thoughts
  - The results you return should be calculated separately from views
  - The results you return won't be shared between other views

  Low-level stuff
    "The context processor'll be executed every time a template is rendered
    using Django's `RequestContext`" (I assume templates use it by default?)

  More info
  - Django already has five availabe (four was shown and an absent 'csrf')
  - Use custom template tag (e.g. {% url 'app:view' %}) if your functionality
    is not needed in ALL templates.

  Lastly, search "Context" on https://devdocs.io/django~2.2/ for MORE info
"""


def cart(request):
    # The 'cart_global' was used to detect if the cart has something, to do
    # that we used a template filter named '|length', it works for dict! The
    # dict I'm talking about is the session 'cart' (inst of 'Cart' (cart.py))
    return {"cart_global": Cart(request)}
