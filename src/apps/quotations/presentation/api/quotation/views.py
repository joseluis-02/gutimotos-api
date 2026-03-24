# Python
import logging
from dataclasses import asdict
# Django rest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.quotations.application.commands.create_quotation_command import CreateQuotationCommand
from apps.quotations.application.commands.update_quotation_status_command import UpdateQuotationStatusCommand
from apps.quotations.application.commands.update_quotation_items_command import UpdateQuotationItemsCommand
from apps.quotations.application.dto.quotation_dto import (
    CreateQuotationRequestDTO,
    QuotationItemRequestDTO,
    UpdateQuotationStatusRequestDTO,
    #Update items
    UpdateQuotationItemsRequestDTO,
    UpdateQuotationItemDTO
)
from apps.quotations.domain.services.price_calculator_service import PriceCalculatorService
from apps.quotations.domain.exceptions.quotation_exception import (
    ProductNotFoundException,
    ProductPriceNotFoundException,
    TypePriceNotFoundException,
    CurrencyNotFoundException,
    QuotationItemDuplicatedException,
    QuotationDomainException,
    InvalidStatusTransitionException,
    QuotationNotFoundException,
    UnauthorizedStatusChangeException,
    InvalidQuotationStateException
)
from apps.quotations.infrastructure.persistence.repositories.quotatio_repository_impl import (
    DjangoProductRepository,
    DjangoTypePriceRepository,
    DjangoCurrencyRepository,
    DjangoQuotationRepository
)
from apps.quotations.presentation.api.quotation.serializers import (
    CreateQuotationRequestSerializer,
    QuotationResponseSerializer,
    UpdateQuotationStatusRequestSerializer,
    UpdateQuotationStatusResponseSerializer,
    UpdateQuotationItemsRequestSerializer
)



class CreateQuotationAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Crea una nueva cotización
        
        Request Body:
        {
            "items": [
                {"product_code": "HBZ-185", "quantity": 5}
            ],
            "type_price_slug": "venta-publico",
            "currency_code": "BOB",
            "whatsapp": "+59112345678"
        }
        
        Returns:
            201: Cotización creada exitosamente
            400: Datos inválidos o error de dominio
            404: Recurso no encontrado (producto, precio, moneda, tipo precio)
            500: Error interno del servidor
        """
        # 1. Validar request con serializer
        serializer = CreateQuotationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        
        try:
            # 2. Construir DTOs
            items_dto = [
                QuotationItemRequestDTO(
                    product_code=item['product_code'],
                    quantity=item['quantity']
                )
                for item in validated_data['items']
            ]
            
            request_dto = CreateQuotationRequestDTO(
                user_id=request.user.id,  # UUID del usuario autenticado
                items=items_dto,
                type_price_slug=validated_data['type_price_slug'],
                currency_code=validated_data['currency_code'],
                whatsapp=validated_data.get('whatsapp')
            )
            
            # 3. Crear instancias de repositorios
            product_repo = DjangoProductRepository()
            type_price_repo = DjangoTypePriceRepository()
            currency_repo = DjangoCurrencyRepository()
            quotation_repo = DjangoQuotationRepository()
            price_calculator = PriceCalculatorService()
            
            # 4. Crear comando y ejecutar
            command = CreateQuotationCommand(
                product_repository=product_repo,
                type_price_repository=type_price_repo,
                currency_repository=currency_repo,
                quotation_repository=quotation_repo,
                price_calculator=price_calculator,
                expiration_days=7  # 7 días de expiración
            )
            
            response_dto = command.execute(request_dto)
            
            # 5. Serializar respuesta
            response_serializer = QuotationResponseSerializer(asdict(response_dto))
            
            return Response(
                {
                    'message': 'Cotización creada exitosamente',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        except ProductNotFoundException as e:
            return Response(
                {
                    'error': 'Producto no encontrado',
                    'details': str(e),
                    'product_code': e.product_code
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        except ProductPriceNotFoundException as e:
            return Response(
                {
                    'error': 'Precio de producto no encontrado',
                    'details': str(e),
                    'product_code': e.product_code,
                    'currency_code': e.currency_code
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        except TypePriceNotFoundException as e:
            return Response(
                {
                    'error': 'Tipo de precio no encontrado',
                    'details': str(e),
                    'slug': e.slug
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        except CurrencyNotFoundException as e:
            return Response(
                {
                    'error': 'Moneda no encontrada',
                    'details': str(e),
                    'code': e.code
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        except QuotationItemDuplicatedException as e:
            return Response(
                {
                    'error': 'Item duplicado',
                    'details': str(e),
                    'product_code': e.product_code
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except QuotationDomainException as e:
            return Response(
                {
                    'error': 'Error en la cotización',
                    'details': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception("Error inesperado al crear cotización")
            
            return Response(
                {
                    'error': 'Error interno del servidor',
                    'details': 'Ocurrió un error inesperado'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PatchQuotationStatusAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, quotation_id):
        """
        Actualiza el estado de una cotización
        
        Request Body:
        {
            "status": "CONFIRMED"
        }
        """
        # 1. Validar request
        serializer = UpdateQuotationStatusRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 2. Construir DTO
            request_dto = UpdateQuotationStatusRequestDTO(
                quotation_id=quotation_id,
                new_status=serializer.validated_data['status'],
                user_id=request.user.id
            )
            
            # 3. Crear repositorio
            quotation_repo = DjangoQuotationRepository()
            
            # 4. Crear comando y ejecutar
            command = UpdateQuotationStatusCommand(quotation_repo)
            response_dto = command.execute(request_dto)
            
            # 5. Serializar respuesta
            response_serializer = UpdateQuotationStatusResponseSerializer(asdict(response_dto))
            
            return Response(
                {
                    'message': 'Estado actualizado exitosamente',
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        except QuotationNotFoundException as e:
            return Response(
                {'error': 'Cotización no encontrada', 'details': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except UnauthorizedStatusChangeException as e:
            return Response(
                {'error': 'No autorizado', 'details': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        
        except InvalidStatusTransitionException as e:
            return Response(
                {'error': 'Transición inválida', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception("Error al actualizar estado")
            
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateQuotationItemsAPIView(APIView):
    """
    API View para actualizar items de cotización
    
    PUT /api/quotation/{id}/items/
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, quotation_id):
        assert request.user.is_authenticated
        """
        Request Body:
        {
            "items": [
                {"product_code": "CG-208", "quantity": 10},
                {"product_code": "WY-022", "quantity": 5},
                {"product_code": "1234-145", "quantity": 6}
            ]
        }
        """
        serializer = UpdateQuotationItemsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Construir DTOs
            items_dto = [
                UpdateQuotationItemDTO(
                    product_code=item['product_code'],
                    quantity=item['quantity']
                )
                for item in serializer.validated_data['items']
            ]
            
            request_dto = UpdateQuotationItemsRequestDTO(
                quotation_id=quotation_id,
                user_id=request.user.id,
                items=items_dto
            )
            
            # Crear repositorios
            quotation_repo = DjangoQuotationRepository()
            product_repo = DjangoProductRepository()
            price_calculator = PriceCalculatorService()
            
            # Ejecutar comando
            command = UpdateQuotationItemsCommand(
                quotation_repository=quotation_repo,
                product_repository=product_repo,
                price_calculator=price_calculator
            )
            
            response_dto = command.execute(request_dto)
            
            # Serializar respuesta
            return Response(
                {
                    'message': 'Items actualizados exitosamente',
                    'data': {
                        'quotation_id': str(response_dto.quotation_id),
                        'subtotal': str(response_dto.subtotal),
                        'total': str(response_dto.total),
                        'items': [
                            {
                                'product_code': item.product_code,
                                'product_description': item.product_description,
                                'quantity': item.quantity,
                                'unit_price': str(item.unit_price),
                                'subtotal': str(item.subtotal)
                            }
                            for item in response_dto.items
                        ]
                    }
                },
                status=status.HTTP_200_OK
            )
        
        except QuotationNotFoundException as e:
            return Response(
                {'error': 'Cotización no encontrada', 'details': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except UnauthorizedStatusChangeException as e:
            return Response(
                {'error': 'No autorizado', 'details': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        
        except InvalidQuotationStateException as e:
            return Response(
                {'error': 'Estado inválido', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except (ProductNotFoundException, ProductPriceNotFoundException, QuotationItemDuplicatedException) as e:
            return Response(
                {'error': str(e.__class__.__name__), 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception("Error actualizando items")
            
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Alias para mantener compatibilidad con urls.py que use nombre de función
create_quotation = CreateQuotationAPIView.as_view()
patch_quotation_status = PatchQuotationStatusAPIView.as_view()
update_quotation_items = UpdateQuotationItemsAPIView.as_view()