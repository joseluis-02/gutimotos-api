# Django rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Serializers
from ..serializers import UserCreateSerializer

# Endpoint para crear un nuevo usuario
class UserCreateAPIView(APIView):
    serializer_class = UserCreateSerializer
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Usuario creado correctamente.",
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "email_verified": user.email_verified,
                }
            }, status=status.HTTP_201_CREATED)

        # Formato personalizado del error
        return Response({
            "message": "Error de validación",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
