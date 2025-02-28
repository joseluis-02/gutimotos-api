# Django rest
from rest_framework.pagination import CursorPagination
# Model MotorcyclePhoto
class MotorcyclePhotoCustomCursorPagination(CursorPagination):
    """
    Paginación de Cursor personalizada para el modelo MotorcyclePhoto.
    Utilizamos `created` como campo de cursor para hacer la paginación eficiente por fecha de creación.
    """
    page_size = 10  # Número de elementos por página
    page_size_query_param = 'page_size'  # Parámetro de la URL para cambiar el tamaño de la página
    max_page_size = 100  # Tamaño máximo de página que se puede pedir
    ordering = ['created']  # Ordenar por fecha de creación de manera ascendente