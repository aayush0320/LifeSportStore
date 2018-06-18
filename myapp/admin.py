from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Product, Category, Client, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)

