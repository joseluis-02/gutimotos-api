# Django
from django.conf import settings
# Twilio
from twilio.rest import Client

class WhatsAppTwilioService:
    @staticmethod
    def send_otp(contact, otp):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        from_number = f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER.strip()}"  # ⚠ strip() elimina espacios invisibles
        to_number = f"whatsapp:{contact.full_number.strip()}"
        #print(f"DEBUG: from={from_number}, to={to_number}")
        client.messages.create(
            from_=from_number,
            to=to_number,
            body=f"Gutimotos te envía tu código de verificación que es: *{otp}* y expira en 2 minutos."
        )
