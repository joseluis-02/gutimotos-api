# Python
import logging
# Django
from django.conf import settings
# Twilio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)

class TwilioService:
    """
    Servicio Twilio para enviar mensajes SMS y WhatsApp
    """

    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_whatsapp_message(self, to_number: str, message: str):
        """
        Envía mensaje de WhatsApp usando Twilio Sandbox o producción.
        """
        try:
            msg = self.client.messages.create(
                from_='whatsapp:' + settings.TWILIO_WHATSAPP_NUMBER,
                to='whatsapp:' + to_number,
                body=message
            )
            return msg.sid
        except TwilioRestException as e:
            logger.error(f"Error enviando WhatsApp a {to_number}: {e}")
            raise ValueError("No se pudo enviar el mensaje por WhatsApp") from e

    def send_sms_message(self, to_number: str, message: str):
        """
        Envía SMS usando Twilio.
        """
        try:
            msg = self.client.messages.create(
                from_=settings.TWILIO_SMS_NUMBER,
                to=to_number,
                body=message
            )
            return msg.sid
        except TwilioRestException as e:
            logger.error(f"Error enviando SMS a {to_number}: {e}")
            raise ValueError("No se pudo enviar el mensaje por SMS") from e
