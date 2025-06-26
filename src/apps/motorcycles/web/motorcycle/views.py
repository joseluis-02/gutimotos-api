# Django
from django.views.generic import TemplateView
# Models
from apps.motorcycles.models import Motorcycle

class MotorcycleTabulatorTemplateView(TemplateView):
    template_name = 'motorcycles/motorcycle/tabulator.html'