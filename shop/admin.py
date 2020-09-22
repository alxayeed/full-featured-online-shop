from django.contrib import admin
from .models import Catagory, Product


@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_field = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'added', 'updated']
    list_filter = ['available', 'added', 'updated']
    list_editable = ['price', 'available']
    prepopulated_field = {'slug': ('name',)}
