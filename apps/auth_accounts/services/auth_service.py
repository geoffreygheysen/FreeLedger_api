from apps.auth_accounts.models import Auth
from django.utils import timezone


class AuthService:
    """
    Service gérant l'enregistrement des utilisateurs.
    """
    @staticmethod
    def register(validated_data):
        manager = Auth.objects
        role = validated_data['role']
        validated_data.pop('role')
        validated_data.pop('password_confirmed')
        if role:
            user = manager.create_superuser(**validated_data)
        else:
            user = manager.create_user(**validated_data)

        # Création de l’utilisateur en transmettant tous les extra_fields
        return user

    @staticmethod
    def update_last_login(user):
        """
        Met à jour le champ last_login de l’utilisateur.
        """
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])