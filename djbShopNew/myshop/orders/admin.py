import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    """
    Don't let these code frighten you, it's actually just two steps,
    get the field name & its correspond data, and then write it to a file.
    """

    # The core of the Django ORM. It enables other parts of
    # the system to understand the capabilities of each model.
    options = modeladmin.model._meta

    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = f"attachment;filename={options.verbose_name}.csv"
    writer = csv.writer(response)

    # A list of '<django.db.models.fields.XxxField: field_name>' strings
    model_fields = [
        field
        for field in options.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]

    # The header
    writer.writerow([field.verbose_name for field in model_fields])

    # The data rows
    for obj in queryset:
        data_row = []
        for field in model_fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)

    return response


def order_detail(obj):
    link_admin_order_detail = reverse(
        viewname="orders:admin_order_detail", args=[obj.id]
    )
    return mark_safe(f"<a href='{link_admin_order_detail}'>View</a>")


def order_pdf(obj):
    link_admin_order_pdf = reverse(
        viewname="orders:admin_order_pdf", args=[obj.id]
    )
    return mark_safe(f"<a href={link_admin_order_pdf}>PDF</a>")


export_to_csv.short_description = "Export to CSV"
order_pdf.short_description = "Invoice"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    list_display = [
        order_detail,
        order_pdf,
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
