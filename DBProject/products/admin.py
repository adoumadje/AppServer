from django.contrib import admin

from .models import Product, Category

# Register your models here.

admin.site.register(Product)  # Registers the Product model in the admin interface
admin.site.register(Category)
