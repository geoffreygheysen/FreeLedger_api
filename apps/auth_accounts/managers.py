from django.contrib.auth.base_user import BaseUserManager
from apps.auth_accounts.models.choices import ROLE_ADMIN


class AuthManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided.')
        if not password:
            raise ValueError('Password must be provided.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if self.model.objects.filter(is_superuser=True).exists():
            raise ValueError('Superuser already exists.')
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)