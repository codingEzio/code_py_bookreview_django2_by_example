from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "coupon_code",
        "valid_from",
        "valid_to",
        "discount",
        "active",
    ]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["coupon_code"]


admin.site.register(Coupon, CouponAdmin)
