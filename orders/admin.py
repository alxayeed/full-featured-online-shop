from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin
from .models import Order, OrderItem

import csv
import datetime
from django.http import HttpResponse


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    # print(opts.verbose_name)
    # content_disposition = 'attachment; filename="some.csv"'
    response = HttpResponse(content_type='text/csv')
    # response['Content-Dispostion'] = content_disposition
    response['Content-Disposition'] = 'attachment; filename="order.csv"'

    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not
              field.many_to_many and not field.one_to_many]

    # write header of the csv acording to model fields names
    writer.writerow([field.verbose_name for field in fields])

    # write data row
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    '''
    Function to display order details in a customized admin  template
    '''
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid', 'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemAdmin]
    actions = [export_to_csv]
