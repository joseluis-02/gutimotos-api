# Django
from django.urls import path
# Views
from .views import MotorcycleTabulatorTemplateView

app_name = 'web_motorcycle' 

urlpatterns = [
    path('motorcycle/tabulator', MotorcycleTabulatorTemplateView.as_view(), name='tabulator'),
]