# apps/users/api/views/update.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# SimpleJWT
from rest_framework_simplejwt.authentication import JWTAuthentication
# Serializers
from ..serializers import UserUpdateSerializer

class UserUpdateAPIView(APIView):
    serializer_class = UserUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,  # Permite actualizar solo algunos campos
            context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Usuario actualizado correctamente.",
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "email_verified": user.email_verified,
                }
            })
        return Response({
            "message": "Error de validación",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
