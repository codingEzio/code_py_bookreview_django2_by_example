from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Add a prefix to all the routes (one way of i18nize URLs)
# Examples:
#   http://localhost:8000/de/
#   http://localhost:8000/en-gb/
#   http://localhost:8000/zh-hant/
urlpatterns = i18n_patterns(
    path(route="admin/", view=admin.site.urls),
    path(route="cart/", view=include(arg="cart.urls", namespace="cart")),
    path(route="orders/", view=include(arg="orders.urls", namespace="orders")),
    path(
        route="coupons/", view=include(arg="coupons.urls", namespace="coupons")
    ),
    path(route="rosetta/", view=include(arg="rosetta.urls")),
    path(route="", view=include("shop.urls", namespace="shop")),
)

if settings.DEBUG:
    import debug_toolbar

    # Third-party debug library
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    # Media (user-uploaded) files
    urlpatterns += static(
        prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
