# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import ProductPhotoReadOnlyModelViewSet

router1 = DefaultRouter(
    trailing_slash=False
)
router1.register(r'product-photo', ProductPhotoReadOnlyModelViewSet, basename='product-photo')

router_urls = router1.urls