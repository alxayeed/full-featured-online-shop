from django.contrib import admin
from .models import Catagory, Product
from parler.admin import TranslatableAdmin


@admin.register(Catagory)
class CatagoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        """
        this method will serve the functionality of prepopulated_fieldss,
        because django-parler admin doesn't support it directly
        """
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'added', 'updated']
    list_filter = ['available', 'added', 'updated']
    list_editable = ['price', 'available']

    def get_prepopulated_fields(self, request, obj=None):
        """
        this method will serve the functionality of prepopulated_fieldss,
        because django-parler admin doesn't support it directly
        """
        return {'slug': ('name',)}
