# Django
from django.contrib import admin
# Models
from .models.brand import Brand
from .models.color import Color
from .models.stock_type import StockType

admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(StockType)

