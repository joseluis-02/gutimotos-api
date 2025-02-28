# Django
from django.shortcuts import render
from django.views.generic import TemplateView
# Views del modelo Brand=Marca
class BrandTemplateView(TemplateView):
    template_name = 'apps/motorcycles/brand/list.html'