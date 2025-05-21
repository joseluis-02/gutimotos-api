# Django
from django.contrib import admin
# Models
from .models import Currency, TypePrice, ExchangeRate

# Register Currency model
admin.site.register(Currency)

# Register TypePrice model
admin.site.register(TypePrice)

# Register ExchangeRate model
admin.site.register(ExchangeRate)
