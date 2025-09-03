from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.auth_accounts.views.auth_view import AuthView

router = DefaultRouter()
router.register(r'', AuthView, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]