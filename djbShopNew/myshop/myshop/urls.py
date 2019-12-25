from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="cart/", view=include(arg="cart.urls", namespace="cart")),
    path(
        route="orders/", view=include(arg="orders.urls", namespace="orders")
    ),
    path(
        route="coupons/",
        view=include(arg="coupons.urls", namespace="coupons"),
    ),
    path(route="", view=include("shop.urls", namespace="shop")),
]

if settings.DEBUG:
    import debug_toolbar

    # Third-party debug library
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    # Media (user-uploaded) files
    urlpatterns += static(
        prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
