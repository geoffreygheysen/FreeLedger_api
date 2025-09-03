from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .choices import ROLE_CHOICES
from apps.auth_accounts.managers import AuthManager


class Auth(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model mappé sur la table `auth_accounts`.
    """
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, db_column='password_hash')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    objects = AuthManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_accounts'
        constraints = [
            models.UniqueConstraint(
                fields=['is_superuser'],
                condition=Q(is_superuser=True),
                name='unique_superuser'
            )
        ]
