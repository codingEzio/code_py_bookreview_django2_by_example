from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Add a prefix to all the routes (one way of i18nize URLs)
# Examples:
#   http://localhost:8000/de/
#   http://localhost:8000/en-gb/
#   http://localhost:8000/zh-hant/
# Another way of i18nize URLs
#   1. _(STUFF_YOU_WANNA_I18NIZE)
#   2. django-admin makemessages --all
urlpatterns = i18n_patterns(
    path(route=_("admin/"), view=admin.site.urls),
    path(route=_("cart/"), view=include(arg="cart.urls", namespace="cart")),
    path(
        route=_("orders/"), view=include(arg="orders.urls", namespace="orders")
    ),
    path(
        route=_("coupons/"),
        view=include(arg="coupons.urls", namespace="coupons"),
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
