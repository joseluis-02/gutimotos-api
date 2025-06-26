# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import MotorcyclePhotoReadOnlyModelViewSet

router1 = DefaultRouter(
    trailing_slash=False
)
router1.register(r'motorcycle-photo', MotorcyclePhotoReadOnlyModelViewSet, basename='motorcycle-photo')

router_urls = router1.urls