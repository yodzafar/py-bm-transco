from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config import settings

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="BM Transco API",
        default_version="v1",
        contact=openapi.Contact(email="yodzafar9966@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger
    path(
        "swagger/",
        schema_view_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/", schema_view_v1.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("api/", include("apps.partners.urls")),
    path("api/", include("apps.site_settings.urls")),
    path("api/", include("apps.services.urls")),
    path("api/", include("apps.messages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
