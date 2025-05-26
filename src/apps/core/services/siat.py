import logging
from zeep import Client, Transport
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

# Configuración de logging
logger = logging.getLogger(__name__)

# URL del WSDL del servicio
WSDL_URL = "https://pilotosiatservicios.impuestos.gob.bo/v2/FacturacionCodigos?wsdl"

class Siat:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Inicializa el cliente Zeep con headers personalizados."""
        session = Session()
        session.verify = True
        session.headers.update({"apiKey": f"TokenApi {self.api_key}"})
        transport = Transport(session=session,timeout=5)
        return Client(WSDL_URL, transport=transport)

    def verificar_nit(self, nit:int):
        """Verifica si un NIT está registrado en el sistema."""
        try:
            #opreancion = self.client.get_type("ns0:verificarNit")
            #print(opreancion)
            solicitud_tipo = self.client.get_type("ns0:solicitudVerificarNit")
            print(solicitud_tipo)
            """
            solicitudVerificarNit({https://siat.impuestos.gob.bo/}solicitudVerificarNit(
                codigoAmbiente: xsd:int, 
                codigoModalidad: xsd:int, 
                codigoSistema: xsd:string, 
                codigoSucursal: xsd:int, 
                cuis: xsd:string, 
                nit: xsd:long, 
                nitParaVerificacion: xsd:long
            ))
            {'success': True, 'data': {}}"""
            # Crear la solicitud con el NIT
            #solicitud = solicitud_tipo(nit=nit)
            # Hacer la solicitud al servicio
            #response = self.client.service.verificarNit(solicitud)
            # Convertir la respuesta en un diccionario serializable
            #data = serialize_object(solicitud_tipo)
            solicitud = solicitud_tipo(
                codigoAmbiente=2,
                codigoModalidad=2,
                codigoSistema='81699A7814CC5D46ED15D76',
                codigoSucursal=0,
                cuis='43FDB877',
                nit=4247012018,
                nitParaVerificacion=nit
                #cuis='43FDB877',
                
                #nitParaVerificacion=8507526016
                
            )
            response = self.client.service.verificarNit(solicitud)
            data = serialize_object(response)
            return { "success":True, "data":data}
        except Fault as e:
            logger.error(f"Error SOAP: {e}")
            return {"success": False, "error": "Error en la solicitud SOAP", "details": str(e)}
        except RequestException as e:
            logger.error(f"Error de conexión: {e}")
            return {"success": False, "error": "Error de conexión con el servicio SIAT", "details": str(e)}

    def verificar_comunicacion(self):
        """Verifica si hay comunicación con el servicio SIAT."""
        try:
            response = self.client.service.verificarComunicacion()
            data = serialize_object(response)
            return { "success":True, "data":data}
            
            #return {"success": True, "data": response}
        except Fault as e:
            logger.error(f"Error SOAP: {e}")
            return {"success": False, "error": "Error en la solicitud SOAP", "details": str(e)}
        except RequestException as e:
            logger.error(f"Error de conexión: {e}")
            return {"success": False, "error": "Error de conexión con el servicio SIAT", "details": str(e)}

    def obtener_cuis(self):
        """Obtiene el código CUIS."""
        try:
            """
            <wsdl:operation name="cuis"> -> Encuentras en el SOAP de Siat
            opreancion = self.client.get_type("ns0:cuis") -> Esto te entrega el nombre de solicitud para obtener que parametros se requiere
            respuesta es :  cuis({https://siat.impuestos.gob.bo/}cuis(SolicitudCuis: {https://siat.impuestos.gob.bo/}solicitudCuis))
                            {'success': True, 'data': {}}
            solicitud_tipo = self.client.get_type("ns0:solicitudCuis") -> Obtiene el tipo de objeto que espera el servicio
            respuesta es:   solicitudCuis({https://siat.impuestos.gob.bo/}solicitudCuis(
                                codigoAmbiente: xsd:int, 
                                codigoModalidad: xsd:int, 
                                codigoPuntoVenta: xsd:int, 
                                codigoSistema: xsd:string, 
                                codigoSucursal: xsd:int, 
                                nit: xsd:long))
                            {'success': True, 'data': {}}
            solicitud = solicitud_tipo(
                codigoAmbiente=2,
                codigoModalidad=2,
                codigoPuntoVenta=0,
                codigoSistema='81699A7814CC5D46ED15D76',
                codigoSucursal=0,
                nit=4247012018
            )
            paso último response = self.client.service.cuis(solicitud)
            """
            # Obtener el tipo de objeto que espera el servicio
            solicitud_tipo = self.client.get_type("ns0:solicitudCuis")
            solicitud = solicitud_tipo(
                codigoAmbiente=2,
                codigoModalidad=2,
                codigoPuntoVenta=0,
                codigoSistema='81699A7814CC5D46ED15D76',
                codigoSucursal=0,
                nit=4247012018
            )
            print(solicitud)
            response = self.client.service.cuis(solicitud)
            data = serialize_object(response)
            return { "success":True, "data":data}
        except Fault as e:
            logger.error(f"Error SOAP: {e}")
            return {"success": False, "error": "Error en la solicitud SOAP", "details": str(e)}
        except RequestException as e:
            logger.error(f"Error de conexión: {e}")
            return {"success": False, "error": "Error de conexión con el servicio SIAT", "details": str(e)}

    def obtener_cufd(self, codigo_sucursal: int, codigo_modalidad: int, cuis: str):
        """Obtiene el código CUFD."""
        try:
            response = self.client.service.cufd(
                codigoSucursal=codigo_sucursal,
                codigoModalidad=codigo_modalidad,
                cuis=cuis
            )
            return {"success": True, "data": response}
        except Fault as e:
            logger.error(f"Error SOAP: {e}")
            return {"success": False, "error": "Error en la solicitud SOAP", "details": str(e)}
        except RequestException as e:
            logger.error(f"Error de conexión: {e}")
            return {"success": False, "error": "Error de conexión con el servicio SIAT", "details": str(e)}
