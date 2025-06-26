# Django REST Framework
from rest_framework.viewsets import ReadOnlyModelViewSet
# Models
from ...models import Motorcycle
# Serializers
from .serializers import MotorcycleTabulatorModelSerializer
# Pagination
from .paginations import MotorcycleTabulatorLimitOffsetPagination

class MotorcycleTabulatroReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Motorcycle.objects.all()
    serializer_class = MotorcycleTabulatorModelSerializer
    pagination_class = MotorcycleTabulatorLimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
