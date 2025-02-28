# Django
from django.contrib import admin
# Models
from .models import Sale, SaleNumber
# Registrando al modelo Sale=Venta
admin.site.register(Sale)
# Registrando al modelo SaleNumber=NumeroVenta
admin.site.register(SaleNumber)