# Django rest-framework
from rest_framework.routers import DefaultRouter
# Views
from .views import BrandViewSet, MotorcyclePhotoViewSet
# ViewSet del modelo Brand=Marca
brands = DefaultRouter()
brands.register(r'brand', BrandViewSet)
# ViewSet del modelo MotorcyclePhoto=FotoMotocicleta
photos = DefaultRouter()
photos.register(r'photo', MotorcyclePhotoViewSet)

# Router
router = brands.urls + photos.urls