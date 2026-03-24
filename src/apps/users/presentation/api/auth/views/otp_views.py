# Python
import logging
# Django rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
# Users - Application
from apps.users.application.services.otp_authentication_service import OTPAuthenticationService
# Users - Domain
from apps.users.domain.exceptions.otp_exceptions import OTPRateLimitException
# Users - Presentation
from apps.users.presentation.api.auth.serializers.otp_serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer
)

logger = logging.getLogger(__name__)


class RequestOTPView(APIView):
    """Endpoint para solicitar código OTP"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/otp/request
        
        Body: {"email": "user@example.com"}
        
        Response:
        {
            "success": true,
            "message": "Código enviado",
            "email": "user@example.com",
            "action": "login|verify|register"
        }
        """
        serializer = RequestOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        
        try:
            service = OTPAuthenticationService()
            result = service.request_otp(email)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        'success': False,
                        'message': result['message'],
                        'error': result.get('error')
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except OTPRateLimitException as e:
            return Response(
                {
                    'success': False,
                    'message': str(e),
                    'error': 'RATE_LIMIT',
                    'retry_after_seconds': e.retry_after_seconds
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        except Exception as e:
            logger.exception(f"Error inesperado: {e}")
            return Response(
                {
                    'success': False,
                    'message': 'Error interno',
                    'error': 'INTERNAL_ERROR'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyOTPView(APIView):
    """Endpoint para verificar código OTP"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        POST /api/auth/otp/verify
        
        Body: {"email": "joseluis_a_@outlook.es", "code": "123456"}
        
        Response:
        {
            "success": true,
            "message": "Código verificado",
            "action": "login|verified|registered",
            "access": "jwt_token",
            "refresh": "jwt_token",
            "user": {...}
        }
        """
        serializer = VerifyOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        
        try:
            service = OTPAuthenticationService()
            result = service.verify_otp(email, code)
            
            if result['success']:
                user = result['user']
                
                # Generar tokens JWT
                refresh = RefreshToken.for_user(user)
                
                return Response(
                    {
                        'success': True,
                        'message': result['message'],
                        'action': result['action'],
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': {
                            'id': str(user.id),
                            'email': user.email,
                            'email_verified': user.email_verified,
                            'is_active': user.is_active
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'success': False,
                        'message': result['message'],
                        'error': result.get('error')
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        except Exception as e:
            logger.exception(f"Error inesperado: {e}")
            return Response(
                {
                    'success': False,
                    'message': 'Error interno',
                    'error': 'INTERNAL_ERROR'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )