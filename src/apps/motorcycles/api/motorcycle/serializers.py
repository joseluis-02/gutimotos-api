# Django REST Framework
from rest_framework import serializers
from ...models import Motorcycle

class MotorcycleTabulatorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        fields = ['id', 'code_dim', 'code_fvr', 'model_year', 'manufacturing_year', 'code_chasis']