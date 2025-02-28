# Django
from django.contrib import admin
# Models
from .models import (
    Category, 
    Importer, 
    Color, 
    Country, 
    Brand, 
    MotorcycleType, 
    TransmissionType, 
    Motorcycle, 
    TypePrice, 
    Currency, 
    MotorcyclePrice, 
    MotorcyclePhoto
)
# Regsitrando al modelo Category=Categoría
admin.site.register(Category)
# Registrando al modelo Importer=Importador
admin.site.register(Importer)
# Registrando al modelo Color=Color
admin.site.register(Color)
# Registrando al modelo Country=País
admin.site.register(Country)
# Registrando al modelo Brand=Marca
admin.site.register(Brand)
# Registrando al modelo MotorcycleType=TipoMotocicleta
admin.site.register(MotorcycleType)
# Registrando al modelo TransmissionType=TipoTransmisión
admin.site.register(TransmissionType)
# Registrando al modelo Motorcycle=Motocicleta
admin.site.register(Motorcycle)
# Registrando al modelo TypePrice
admin.site.register(TypePrice)
# Registrando al modelo Currency=Divisa
admin.site.register(Currency)
# Registrando al modelo MotorcyclePrice=PrecioMotocicleta
admin.site.register(MotorcyclePrice)
# Registrando al modelo MotorcyclePhoto=FotoMotocicleta
admin.site.register(MotorcyclePhoto)
