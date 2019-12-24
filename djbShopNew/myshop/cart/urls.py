from django.urls import path
from . import views


app_name = "cart"


urlpatterns = [
    path(route="", view=views.cart_detail, name="cart_detail"),
    path(
        route="add/<int:product_id>/", view=views.cart_add, name="cart_add"
    ),
    path(
        route="remove/<int:product_id>/",
        view=views.cart_remove,
        name="cart_remove",
    ),
]
