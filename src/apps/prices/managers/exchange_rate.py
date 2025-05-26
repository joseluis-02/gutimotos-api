# Django
from django.db import models

# Manejador para el tipo de cambio
class ExchangeRateManager(models.Manager):
    def convert(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        rate = self.get(from_currency=from_currency, to_currency=to_currency).rate
        return amount * rate