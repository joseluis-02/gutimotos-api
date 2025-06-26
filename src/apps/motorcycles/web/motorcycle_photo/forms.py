# Django
from django import forms
# Models
from src.apps.motorcycles.models.motorcycle_photo import MotorcyclePhoto

class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = MotorcyclePhoto
        fields = ['photo', 'motorcycle_file']