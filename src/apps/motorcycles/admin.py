# Django
from django.contrib import admin
# Models
from .models import (
    MotorcycleType, 
    TransmissionType, 
    Motorcycle, 
    MotorcyclePhoto,
    MotorcyclePrice
)

# Registrando al modelo MotorcycleType=TipoMotocicleta
admin.site.register(MotorcycleType)
# Registrando al modelo TransmissionType=TipoTransmisión
admin.site.register(TransmissionType)
# Registrando al modelo Motorcycle=Motocicleta
admin.site.register(Motorcycle)
# Registrando al modelo MotorcyclePhoto=FotoMotocicleta
admin.site.register(MotorcyclePhoto)
# Registrando al modelo MotorcyclePrice=PrecioMotocicleta
admin.site.register(MotorcyclePrice)
