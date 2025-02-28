# Django
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     # URLs regulares de la app motorcycles
     path('motorcycles/', include('apps.motorcycles.urls', namespace='motorcycles')),
     # URLs API de la app blog (versión 1)
     path("motorcycles/api/", include("apps.motorcycles.api.urls", namespace="motorcycles_api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)