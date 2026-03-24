# Python
import logging
# Django
from django.template.loader import render_to_string
# Weasyprint
from weasyprint import HTML, CSS

logger = logging.getLogger(__name__)

class PDFService:
    """Servicio reutilizable para generación de PDFs"""
    
    @staticmethod
    def generate_pdf_from_template(
        template_name: str,
        context: dict,
        css_string: str = None
    ) -> bytes:
        """
        Genera PDF desde template Django
        
        Args:
            template_name: Ruta del template
            context: Contexto para el template
            css_string: CSS adicional (opcional)
            
        Returns:
            Bytes del PDF generado
        """
        try:
            # Renderizar HTML
            html_string = render_to_string(template_name, context)
            
            # Generar PDF
            html = HTML(string=html_string)
            
            if css_string:
                css = CSS(string=css_string)
                pdf_bytes = html.write_pdf(stylesheets=[css])
            else:
                pdf_bytes = html.write_pdf()
            
            logger.info(f"PDF generado exitosamente desde {template_name}")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generando PDF: {str(e)}")
            raise