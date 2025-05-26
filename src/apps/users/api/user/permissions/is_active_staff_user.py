# Django rest framework
from rest_framework.permissions import BasePermission

# Permiso que controla si el usuario es de is_staff=True
class IsActiveStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            # Esto es una propiedad de AbstractBaseUser de Django
            request.user.is_authenticated and
            request.user.is_active and
            request.user.is_staff
        )
