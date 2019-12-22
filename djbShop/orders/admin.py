import csv
import datetime

from django.http import HttpResponse
from django.contrib import admin

from .models import Order, OrderItem


def export_to_csv(model_admin, request, queryset):
    opts = model_admin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        f'attachment;filename={opts.verbose_name}.csv'
    writer = csv.writer(response)

    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'paid', 'city',
                    'address', 'postal_code', 'created', 'updated')
    list_filter = ('paid', 'created', 'updated')
    inlines = [OrderItemInline]


export_to_csv.description = 'Export to CSV'
