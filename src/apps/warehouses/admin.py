# Django
from django.contrib import admin
# Models
from .models import Company, Branch, MotorcycleInventory
# Registrando al modelo Company=Empresa
admin.site.register(Company)
# Registrando al modelo Branch=Sucursal
admin.site.register(Branch)
# Registrando al modelo MotorcycleInventory=InventarioMotocicleta
admin.site.register(MotorcycleInventory)