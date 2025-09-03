from rest_framework.permissions import BasePermission
from apps.auth_accounts.models.choices import ROLE_ADMIN


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == ROLE_ADMIN
        )