# quotations/domain/services/quotation_pdf_service.py

from apps.core.services.pdf_service import PDFService


class QuotationPDFService:
    """Servicio de dominio para generar PDFs de cotizaciones"""
    
    CSS_CARTA = """
        @page {
            size: letter;
            margin: 2cm;
        }
        body {
            font-family: Arial, sans-serif;
            font-size: 12pt;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .quotation-info {
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .total {
            text-align: right;
            font-weight: bold;
            margin-top: 20px;
        }
    """
    
    @staticmethod
    def generate_quotation_pdf(quotation, items: list) -> bytes:
        context = {
            'quotation': quotation,
            'items': items,
            'company_name': 'Gutimotos S.R.L.',  # Configurar
            'company_address': 'Avenida circunvalación y San Cristobal',
            'company_phone': '67398260',
        }
        
        return PDFService.generate_pdf_from_template(
            template_name='quotations/pdf/quotation_pdf.html',
            context=context,
            css_string=QuotationPDFService.CSS_CARTA
        )