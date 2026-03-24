# Python
import logging
# Services
from apps.core.services.email_service import EmailService
from apps.core.services.pdf_service import PDFService

logger = logging.getLogger(__name__)

class PDFMailer:
    """
    Servicio genérico para enviar PDFs por correo.
    """
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def send_pdf_email(
        self,
        subject: str,
        recipients: list,
        pdf_template: str,
        pdf_context: dict,
        email_template: str = None,
        email_context: dict = None,
        filename: str = "document.pdf",
        css_file: str = None,
        page_size: str = "A4"
    ):
        try:
            pdf_file = PDFService.generate_pdf(
                template=pdf_template,
                context=pdf_context,
                css_file=css_file,
                page_size=page_size
            )
            attachments = [(filename, pdf_file, "application/pdf")]

            return self.email_service.send_email(
                subject=subject,
                recipients=recipients,
                html_template=email_template,
                context=email_context,
                attachments=attachments
            )
        except Exception as e:
            logger.error(f"Error enviando correo con PDF a {recipients}: {e}", exc_info=True)
            raise