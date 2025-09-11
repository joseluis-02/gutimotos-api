# Django REST Framework
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class BrandPageNumberPagination(PageNumberPagination):
    # Número de registros por página por defecto
    page_size = 5
    # Nombre del parámetro para que el cliente cambie el tamaño de página: ?limit=10
    page_size_query_param = 'limit'
    # Tamaño máximo que puede pedir el cliente
    max_page_size = 20
    # Nombre del parámetro que identifica la página: ?page=2
    page_query_param = 'page'
    # Respuesta de paginación personalizada (opcional)
    def get_paginated_response(self, data):
        return Response({
            'next_page': self.page.next_page_number() if self.page.has_next() else None,
            'results': data
        })