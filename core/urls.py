from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('apps.auth_accounts.urls')),
]

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView,
    )

    urlpatterns += [
        # Schéma OpenAPI brut
        path(
            'api/schema/',
            SpectacularAPIView.as_view(),
            name='schema'
        ),

        # UI Swagger interactive
        path(
            'api/docs/swagger/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui'
        ),

        # UI Redoc interactive
        path(
            'api/docs/redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc'
        ),
    ]