from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("shop.urls", namespace="shop")),
]

if settings.DEBUG:
    import debug_toolbar

    # Third-party debug library
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    # Media (user-uploaded) files
    urlpatterns += static(
        prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

