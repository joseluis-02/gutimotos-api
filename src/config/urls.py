# Django
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashboard
    path("", include("apps.dashboard.urls", namespace="dashboard")),
    # Core
    path("core/", include("apps.core.urls", namespace="core")),
    # App users}
    path("users/", include("apps.users.urls", namespace="users")),
    # App products
    path("products/", include("apps.products.urls", namespace="products")),
    # App motorcycles
    path("motorcycles/", include("apps.motorcycles.urls", namespace="motorcycles")),
    
    # v2
    path("quotations/", include("apps.quotations.presentation.api.quotation.urls", namespace="quotation")),
    path("users/", include("apps.users.presentation.api.auth.urls", namespace="auth")),
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")),)  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)