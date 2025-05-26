# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import MotorcyclePhotoViewSet
# ViewSet del modelo MotorcyclePhoto=FotoMotocicleta
# trailing_slash=False
#photos = DefaultRouter()
#photos.register(r'', MotorcyclePhotoViewSet)

# Router
#router = photos.urls

router = DefaultRouter()
router.register(r'motorcycle-photo', MotorcyclePhotoViewSet, basename='motorcycle-photo')