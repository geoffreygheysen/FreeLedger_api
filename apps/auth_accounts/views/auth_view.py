from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from apps.auth_accounts.serializers.auth_serializer import AuthSerializer, RegisterSerializer
from apps.auth_accounts.services.auth_service import AuthService


class AuthView(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Obtenir un pair de tokens JWT",
        description=(
                "Requête JSON\n"
                "{ 'email': str, 'password': str }\n\n"
                "Réponse JSON\n"
                "{ 'access': str, 'refresh': str }"
        ),
        request=TokenObtainPairSerializer,
        responses={
            200: OpenApiResponse(description="Tokens JWT émis"),
            401: OpenApiResponse(description="Email ou mot de passe incorrect"),
        },
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], url_path="token")
    def token(self, request):
        """
        Expose `/api/auth/token/` :
        utilise TokenObtainPairSerializer pour générer access + refresh.
        """
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Récupération de l'utilisateur authentifié
        user = serializer.user

        # Mise à jour du last_login
        AuthService.update_last_login(user)

        # Construction de la réponse finale
        data = {
            **serializer.validated_data,
            **AuthSerializer(user).data
        }
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Rafraîchir le token d’accès",
        description=(
                "Requête JSON\n"
                "{ 'refresh': str }\n\n"
                "Réponse JSON\n"
                "{ 'access': str }"
        ),
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(description="Nouveau token d’accès émis"),
            401: OpenApiResponse(description="Refresh token invalide ou expiré"),
        },
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], url_path="token/refresh")
    def token_refresh(self, request):
        """
        Expose `/api/auth/token/refresh/` :
        utilise TokenRefreshSerializer pour générer un nouvel access token.
        """
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Inscription d’un nouvel utilisateur",
        description=(
            "Requête : email, password et password_confirmed. "
            "Réponse : id, email et role."
        ),
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: OpenApiResponse(description="Payload invalide"),
            409: OpenApiResponse(description="Email déjà utilisé"),
        },
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.register(serializer.validated_data)

        # Le même serializer, mais il ne renverra que les champs read_only/readable
        return Response(
            AuthSerializer(user).data,
            status=status.HTTP_201_CREATED
        )