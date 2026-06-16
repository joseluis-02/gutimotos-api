
class OTPException(Exception):
    """Excepción base para errores de OTP"""
    pass


class OTPRateLimitException(OTPException):
    """Se excedió el límite de solicitudes"""
    
    def __init__(self, retry_after_seconds: int = 300):
        self.retry_after_seconds = retry_after_seconds
        super().__init__(
            f"Demasiadas solicitudes. Intenta en {retry_after_seconds // 60} minutos"
        )


class OTPInvalidException(OTPException):
    """Código OTP inválido o expirado"""
    pass


class OTPAttemptsExceededException(OTPException):
    """Se excedieron los intentos permitidos"""
    pass