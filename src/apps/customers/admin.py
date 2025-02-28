# Django
from django.contrib import admin
# Models
from .models import Customer
# Restrando al modelo Customer
admin.site.register(Customer)