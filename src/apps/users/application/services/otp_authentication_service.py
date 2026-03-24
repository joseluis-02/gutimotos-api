# Python
import logging
# Django
from django.utils import timezone
# Users - Domain
from apps.users.domain.services.otp_generator_service import OTPGeneratorService
from apps.users.domain.services.otp_email_service import OTPEmailService
from apps.users.domain.exceptions.otp_exceptions import OTPRateLimitException
# Users - Infrastructure
from apps.users.infrastructure.persistence.repositories.otp_repository_impl import OTPRepositoryImpl
from apps.users.infrastructure.persistence.models.otp import OTP
# Users - Models
from apps.users.models.user import User


logger = logging.getLogger(__name__)

class OTPAuthenticationService:
    """
    Servicio de aplicación para autenticación OTP
    Flujo unificado:
    1. Usuario verificado → Login con OTP
    2. Usuario no verificado → Verificación con OTP
    3. Usuario nuevo → Registro automático con OTP
    
    Características:
    - Rate limiting (3 solicitudes / 5 minutos)
    - Códigos de un solo uso
    - Expiración configurable (10 minutos)
    - Límite de intentos fallidos (5)
    """
    # Configuración
    MAX_REQUESTS_PER_WINDOW = 3
    RATE_LIMIT_WINDOW_MINUTES = 5
    OTP_VALIDITY_MINUTES = 10
    
    def __init__(self):
        self.repository = OTPRepositoryImpl()

    def request_otp(self, email: str) -> dict:
        try:
            email = email.lower().strip()
            
            # Verificar rate limiting
            self._check_rate_limit(email)
            
            # Determinar tipo de usuario
            action = self._determine_action(email)
            
            # Generar y guardar código
            code = self._create_otp_code(email)
            
            # Enviar email
            self._send_otp_email(email, code, action)
            
            logger.info(f"OTP solicitado: {email} (action: {action})")
            
            return {
                'success': True,
                'message': 'Código enviado a tu email',
                'email': email,
                'action': action
            }
            
        except OTPRateLimitException:
            raise
        except Exception as e:
            logger.exception(f"Error solicitando OTP para {email}: {str(e)}")
            return {
                'success': False,
                'message': 'Error al solicitar código',
                'error': 'SERVER_ERROR'
            }
    
    def verify_otp(self, email: str, code: str) -> dict:
        try:
            email = email.lower().strip()
            code = code.strip()
            
            # Buscar OTP válido
            otp = self.repository.find_valid(email, code)
            
            if not otp:
                self._increment_failed_attempts(email, code)
                logger.warning(f"Código inválido: {email}")
                return {
                    'success': False,
                    'message': 'Código inválido o expirado',
                    'error': 'INVALID_CODE'
                }
            
            # Marcar como usado
            otp.mark_as_used()
            
            # Procesar usuario según su estado
            user, action = self._process_user(email)
            
            logger.info(f"OTP verificado: {email} (action: {action})")
            
            return {
                'success': True,
                'message': 'Código verificado',
                'user': user,
                'action': action
            }
            
        except Exception as e:
            logger.exception(f"Error verificando OTP para {email}: {str(e)}")
            return {
                'success': False,
                'message': 'Error al verificar código',
                'error': 'SERVER_ERROR'
            }
    
    # Métodos privados - Lógica interna
    
    def _check_rate_limit(self, email: str) -> None:
        recent_count = self.repository.count_recent(
            email,
            minutes=self.RATE_LIMIT_WINDOW_MINUTES
        )
        
        if recent_count >= self.MAX_REQUESTS_PER_WINDOW:
            logger.warning(f"Rate limit excedido: {email}")
            raise OTPRateLimitException(
                retry_after_seconds=self.RATE_LIMIT_WINDOW_MINUTES * 60
            )
    
    def _determine_action(self, email: str) -> str:
        try:
            user = User.objects.get(email=email)
            return 'login' if user.email_verified else 'verify'
        except User.DoesNotExist:
            return 'register'
    
    def _create_otp_code(self, email: str) -> str:
        """
        Genera código OTP y lo guarda en base de datos
        
        Proceso:
        1. Invalida códigos anteriores activos
        2. Genera nuevo código seguro
        3. Guarda en BD con tiempo de expiración
        
        Returns:
            Código OTP de 6 dígitos
        """
        # Invalidar códigos anteriores
        self.repository.invalidate_previous(email)
        
        # Generar código usando servicio de dominio
        code = OTPGeneratorService.generate_code()
        
        # Guardar en base de datos
        expired = OTP.get_expiration_time(minutes=self.OTP_VALIDITY_MINUTES)
        self.repository.create(email, code, expired)
        
        return code
    
    def _send_otp_email(self, email: str, code: str, action: str) -> None:
        """
        Envía email con código OTP usando servicio de dominio
        
        Args:
            email: Email destinatario
            code: Código OTP
            action: Tipo de acción (para logging)
        """
        email_sent = OTPEmailService.send_otp_email(
            email=email,
            otp_code=code,
            action=action,
            validity_minutes=self.OTP_VALIDITY_MINUTES
        )
        
        if not email_sent:
            logger.error(f"Falló el envío de email a {email}")
    
    def _process_user(self, email: str) -> tuple:
        """
        Procesa usuario según su estado actual
        
        Casos:
        1. Usuario no verificado → Verifica y activa
        2. Usuario verificado → Solo retorna (login)
        3. Usuario no existe → Crea nuevo verificado
        
        Returns:
            Tuple (user: User, action: str)
        """
        try:
            user = User.objects.get(email=email)
            
            # Si no estaba verificado, verificar ahora
            if not user.email_verified:
                user.email_verified = True
                user.is_active = True
                user.save(update_fields=['email_verified', 'is_active'])
                logger.info(f"Usuario verificado: {email}")
                return user, 'verified'
            
            # Usuario ya verificado (login normal)
            return user, 'login'
            
        except User.DoesNotExist:
            # Crear usuario nuevo ya verificado
            user = User.objects.create(
                email=email,
                auth_provider=None,
                email_verified=True,
                is_active=True
            )
            logger.info(f"Usuario registrado: {email}")
            return user, 'registered'
    
    def _increment_failed_attempts(self, email: str, code: str) -> None:
        """
        Incrementa contador de intentos fallidos del OTP
        
        Esto previene ataques de fuerza bruta limitando
        intentos a 5 por código.
        """
        try:
            failed_otp = OTP.objects.get(
                email=email,
                code=code,
                is_used=False
            )
            failed_otp.increment_attempts()
        except OTP.DoesNotExist:
            pass