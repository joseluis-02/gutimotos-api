# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import TypePriceReadOnlyModelViewSet

router1 = DefaultRouter(
    trailing_slash=False
)
router1.register(r'type-price', TypePriceReadOnlyModelViewSet, basename='type-price')

router_urls = router1.urls