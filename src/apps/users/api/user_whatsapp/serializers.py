from rest_framework import serializers
from phonenumbers import parse, is_valid_number, NumberParseException

ALLOWED_COUNTRY_CODES = [54, 591]  # Argentina y Bolivia

class WhatsAppRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        error_messages={
            "blank": "Debes ingresar un número de teléfono.",
            "required": "El campo 'phone_number' es requerido.",
        }
    )
    def validate_phone_number(self, value):
        try:
            pn = parse(value, None)
        except NumberParseException:
            raise serializers.ValidationError(
                "Número inválido o formato incorrecto. Debe estar en formato E.164, ejemplo '+591XXXXXXXX'."
            )
        if pn.country_code not in ALLOWED_COUNTRY_CODES:
            raise serializers.ValidationError("Solo se permiten números de Argentina o Bolivia.")
        if not is_valid_number(pn):
            raise serializers.ValidationError("Número de contacto es inválido")
        # Retorna el número en formato E.164
        return f"+{pn.country_code}{pn.national_number}"


class WhatsAppVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        error_messages={
            "blank": "Debes ingresar un número de teléfono.",
            "required": "El campo 'phone_number' es requerido."
        }
    )
    otp = serializers.CharField(
        max_length=6,
        required=True,
        error_messages={
            "blank": "El código OTP no puede estar vacío.",
            "required": "El campo 'otp' es requerido."
        }
    )
    def validate_phone_number(self, value):
        try:
            pn = parse(value, None)
        except NumberParseException:
            raise serializers.ValidationError(
                "Número inválido o formato incorrecto. Debe estar en formato E.164, ejemplo '+591XXXXXXXX'."
            )
        return f"+{pn.country_code}{pn.national_number}"
