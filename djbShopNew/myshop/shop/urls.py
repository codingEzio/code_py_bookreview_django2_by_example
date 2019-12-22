from django.urls import path
from . import views


app_name = "shop"


urlpatterns = [
    path(route="", view=views.product_list, name="product_list"),
    path(
        route="<slug:category_slug>/",
        view=views.product_list,
        name="product_list_by_category",
    ),
    path(
        route="<int:id>/<slug:slug>/",
        view=views.product_detail,
        name="product_detail",
    ),
]
