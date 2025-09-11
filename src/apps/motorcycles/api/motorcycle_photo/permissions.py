# Django rest framework
from rest_framework import permissions

class IsAuthenticatedRetrieveOnly(permissions.BasePermission):
    """
    Permite acceso solo a retrieve si el usuario está autenticado,
    de lo contrario deja cualquier otra acción pública.
    """
    def has_permission(self, request, view):
        if view.action == 'retrieve':
            return request.user and request.user.is_authenticated
        return True
