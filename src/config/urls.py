# Django
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # App products
    path("", include("apps.products.urls", namespace="products")),
    # App motorcycles
    path("", include("apps.motorcycles.urls", namespace="motorcycles")),
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")),)  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)