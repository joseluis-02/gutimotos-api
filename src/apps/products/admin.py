# Django
from django.contrib import admin
# Models
from .models import Product, ProductPhoto, ProductPrice, ProductStock

admin.site.register(Product)
admin.site.register(ProductPhoto)
admin.site.register(ProductPrice)
admin.site.register(ProductStock)
