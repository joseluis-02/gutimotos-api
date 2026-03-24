# Python
import secrets

class OTPGeneratorService:
    @staticmethod
    def generate_code(length: int = 6) -> str:
        """
        Genera código OTP aleatorio seguro
        
        Args:
            length: Longitud del código (default: 6)
            
        Returns:
            Código numérico de 6 dígitos
            
        Example:
            >>> OTPGeneratorService.generate_code()
            '042791'
        """
        max_value = 10 ** length
        code_int = secrets.randbelow(max_value)
        return str(code_int).zfill(length)