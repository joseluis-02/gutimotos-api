# Django
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# Django rest
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Simple JWT
from rest_framework_simplejwt.authentication import JWTAuthentication
# Models
from ...models.user_whatsapp import UserWhatsApp

# Serializers
from .serializers import WhatsAppRegisterSerializer, WhatsAppVerifySerializer
# Services
from ...services.user_whatsapp.otp import send_otp
# User
User = get_user_model()

class WhatsAppRegisterView(generics.GenericAPIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    serializer_class = WhatsAppRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        raw_number = serializer.validated_data["phone_number"]
        # user = request.user
        email = "gutisoft.dev@gmail.com"
        user = get_object_or_404(User, email=email)

        country_code, number, full_number = UserWhatsApp.normalize_number(raw_number)

        contact, created = UserWhatsApp.objects.get_or_create(
            user=user,
            full_number=full_number,
            defaults={"country_code": country_code, "number": number}
        )

        if contact.verified:
            return Response({
                "whatsapp": "verified",
            }, status=200)
            
        send_otp(contact)

        return Response({
            "whatsapp": "created",
        }, status=200)

class WhatsAppVerifyView(generics.GenericAPIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    serializer_class = WhatsAppVerifySerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp"]
        # user = request.user
        email = "gutisoft.dev@gmail.com"
        user = get_object_or_404(User, email=email)
        _, _, full_number = UserWhatsApp.normalize_number(raw_number)
        try:
            contact = UserWhatsApp.objects.get(user=user, full_number=full_number)
        except UserWhatsApp.DoesNotExist:
            return Response({
                "detail": "Número no registrado"
            }, status=404)
        if contact.verified:
            return Response({
                "whatsapp": "verified",
            }, status=200)
        if contact.otp_is_valid(otp):
            contact.verify()
            return Response({
                "whatsapp": "verified",
            }, status=200)
        return Response({
            "status": "Código de verificación expirado o inválido."
        }, status=400)
