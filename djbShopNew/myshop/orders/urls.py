from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path(route="create/", view=views.order_create, name="order_create")
]
