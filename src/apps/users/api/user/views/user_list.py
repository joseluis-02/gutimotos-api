# Django rest framework
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
# SimpleJWT
from rest_framework_simplejwt.authentication import JWTAuthentication
# Serializers
from ..serializers import UserListSerializer
# Permissions
from ..permissions import IsActiveStaffUser
# Paginations
from ..paginations import UserListCursorPagination
# Models
from ....models import User

# User UserListAPIView
class UserListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsActiveStaffUser]
    serializer_class = UserListSerializer
    pagination_class = UserListCursorPagination  # Usa la paginación de cursor
    queryset = User.objects.only('id', 'email', 'is_active', 'created').order_by('-created')  # Usa el índice