# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import ColorReadOnlyModelViewSet

router1 = DefaultRouter(
    trailing_slash=False
)
router1.register(r'color', ColorReadOnlyModelViewSet, basename='color')

router_urls = router1.urls