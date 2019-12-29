from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ["name", "slug"]

    # Same functionality as attr 'prepopulated_fields'
    # The reason is django-parler only supports the way of using method
    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ["name", "slug", "price", "available", "created", "updated"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}
