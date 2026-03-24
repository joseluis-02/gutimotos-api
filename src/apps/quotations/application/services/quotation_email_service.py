# Core
from apps.core.services.email_service import EmailService
from apps.quotations.domain.services.quotation_pdf_service import QuotationPDFService


class QuotationEmailService:
    """Servicio de aplicación para envío de emails de cotizaciones"""
    
    @staticmethod
    def send_quotation_confirmation_email(quotation, items: list) -> bool:
        """
        Envía email de confirmación con PDF adjunto
        
        Args:
            quotation: Objeto Quotation
            items: Lista de items
            
        Returns:
            True si se envió correctamente
        """
        # Generar PDF
        pdf_bytes = QuotationPDFService.generate_quotation_pdf(quotation, items)
        
        # Preparar email
        subject = 'Su cotización fue confirmada'
        html_content = f"""
                        <!DOCTYPE html>
                        <html lang="es">
                        <head>
                            <meta charset="UTF-8">
                            <title>Cotización Confirmada</title>
                        </head>
                        <body style="margin:0; padding:0; background-color:#f5f5f5; font-family:Arial, Helvetica, sans-serif;">
                        <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="background-color:#f5f5f5;">
                            <tr>
                                <td align="center" style="padding:20px 10px;">

                                    <!-- Container -->
                                    <table width="100%" cellpadding="0" cellspacing="0" role="presentation"
                                        style="max-width:600px; background-color:#ffffff; border-radius:8px; padding:24px; border:1px solid #e5e7eb;">
                                        <!-- Body -->
                                        <tr>
                                            <td>
                                                <p style="margin:0 0 14px; font-size:14px; line-height:1.6; color:#111827;">
                                                    Hemos recibido la confirmación de su cotización.
                                                </p>

                                                <table width="100%" cellpadding="0" cellspacing="0" role="presentation"
                                                    style="margin-bottom:16px; background-color:#f9fafb; border-radius:6px; padding:12px;">
                                                    <tr>
                                                        <td style="font-size:13px; color:#374151; padding-bottom:6px;">
                                                            <strong>Cotización:</strong> #{ quotation.id }
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="font-size:16px; font-weight:700; color:#dc2626;">
                                                            Total: { quotation.currency_code } { quotation.total }
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>

                                        <!-- Footer -->
                                        <tr>
                                            <td style="padding-top:24px; text-align:center;">
                                                <p style="margin:0; font-size:12px; color:#6b7280;">
                                                    Adjuntamos el documento en formato PDF con el detalle completo.
                                                </p>
                                            </td>
                                        </tr>

                                    </table>

                                </td>
                            </tr>
                        </table>
                        </body>
                        </html>
                        """
        
        # Enviar email
        return EmailService.send_email_with_attachment(
            to_email=quotation.user.email,
            subject=subject,
            html_content=html_content,
            attachment_data=pdf_bytes,
            attachment_name=f'cotizacion_{quotation.id}.pdf',
            attachment_type='application/pdf'
        )