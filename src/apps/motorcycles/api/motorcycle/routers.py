# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import MotorcycleTabulatroReadOnlyModelViewSet

motorcycle_tabulator = DefaultRouter(
    trailing_slash=False
)
motorcycle_tabulator.register(r'motorcycle/tabulator', MotorcycleTabulatroReadOnlyModelViewSet, basename='tabulator')