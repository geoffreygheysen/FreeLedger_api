from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.auth_accounts.models import Auth
from apps.auth_accounts.services.auth_service import AuthService


# Regex pour :
# - au moins 8 caractères
# - une minuscule
# - une majuscule
# - un chiffre
# - un caractère spécial parmi @$!%*?&
password_regex = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
    message=(
        "Le mot de passe doit faire au moins 8 caractères, "
        "contenir une majuscule, une minuscule, un chiffre et un caractère spécial (@$!%*?&)."
    )
)

class AuthSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour exposer les données du modèle Auth.
    """
    class Meta:
        model = Auth
        # On liste tout ce qu’on veut gérer
        fields = ['id', 'email']
        read_only_fields = ['id']


class RegisterSerializer(serializers.Serializer):
    """
    Sérialiseur pour valider l'enregistrement d'un nouvel Auth.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[password_regex])
    password_confirmed = serializers.CharField(write_only=True, required=True)
    role = serializers.BooleanField(default=False)

    def validate_email(self, value):
        # normalisation + unicité
        email = Auth.objects.normalize_email(value)
        if Auth.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": ["Cet email est déjà utilisé."]}
            )
        return email

    def validate(self, attrs):
        # vérification de correspondance des mots de passe
        pwd  = attrs.get("password")
        pwd2 = attrs.get("password_confirmed")
        if pwd != pwd2:
            raise serializers.ValidationError(
                {"password": ["Les mots de passe ne correspondent pas."]}
            )
        return attrs

    def create(self, validated_data):
        # on supprime le champ de confirmation avant création
        validated_data.pop("password_confirmed")
        try:
            return AuthService.register(
                email=validated_data["email"],
                password=validated_data["password"],
            )
        except DjangoValidationError as exc:
            # capture d'éventuelles erreurs de création (doublons, etc.)
            raise serializers.ValidationError({"email": exc.messages})