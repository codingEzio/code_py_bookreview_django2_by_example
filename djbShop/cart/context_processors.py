"""
A context processor is a func that receives the `request` object as a param
and returns a dict that gets added to template context (e.g. context={'cart': cart})
which will be available to all the templates using RequestContext (enabled by def)

You might want a custom template tag if your functionality is not needed
in all templates, especially it involves database queries!
"""
from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
