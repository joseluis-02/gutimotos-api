# Django
from django.contrib import admin

admin.site.site_header = "Panel de Administración - Gutimotos"
admin.site.site_title = "Gutimotos Admin"
admin.site.index_title = "Bienvenido al administrador de Gutimotos"

# Models
from .models.brand import Brand
from .models.color import Color
from .models.stock_type import StockType

admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(StockType)

