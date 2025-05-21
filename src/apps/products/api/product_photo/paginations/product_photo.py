# Django rest framework
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
# Utils
from apps.core.utils import extract_cursor

# User List cursor pagination
class ProductPhotoListCursorPagination(CursorPagination):
    page_size = 10  # Número de elementos por página
    max_page_size = 50  # Tamaño máximo de página que se puede pedir
    cursor_query_param = 'cursor' # Define el nombre del parámetro en la URL
    page_size_query_param = 'limit'  # /api/users/?limit=50
    ordering = ['-created']  # Ordenar por fecha de creación de manera ascendente
    # Personaliza la respuesta de paginación
    def get_paginated_response(self, data):
        return Response({
            'next_cursor':  extract_cursor(self.get_next_link(), self.cursor_query_param),
            'previous_cursor': extract_cursor(self.get_previous_link(), self.cursor_query_param),
            'data': data,
        })