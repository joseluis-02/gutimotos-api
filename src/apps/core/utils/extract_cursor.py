# Python
from urllib.parse import urlparse, parse_qs

# Función para extraer el valor del cursor ya sea next o previous
# recibe la URL y el nombre del parámetro del cursor
# nombre del parámetro del cursor_query_name por defecto es 'cursor'
def extract_cursor(url, cursor_query_param='cursor'):
    if not url:
        return None
    return parse_qs(urlparse(url).query).get(cursor_query_param, [None])[0]
