from django.utils.translation import gettext_lazy as _
from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path(route=_("create/"), view=views.order_create, name="order_create"),
    path(
        route="admin/order/<int:order_id>/",
        view=views.admin_order_detail,
        name="admin_order_detail",
    ),
    path(
        route="admin/order/<int:order_id>/pdf/",
        view=views.admin_order_pdf,
        name="admin_order_pdf",
    ),
]
