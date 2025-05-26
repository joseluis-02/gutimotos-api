# Django
from django.contrib import admin
# Models
from .models import Purchase, PurchaseNumber
# Registrando al modelo Purchase
admin.site.register(Purchase)
# Registrando al modelo PurchaseNumber=NúmeroCompra
admin.site.register(PurchaseNumber)