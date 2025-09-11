# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import BrandSelectReadOnlyModelViewSet

router1 = DefaultRouter(
    trailing_slash=False
)
router1.register(r'brand', BrandSelectReadOnlyModelViewSet, basename='brand')

router_urls = router1.urls