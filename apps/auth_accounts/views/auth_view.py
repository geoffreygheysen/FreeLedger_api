from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.auth_accounts.serializers.auth_serializer import AuthSerializer, RegisterSerializer
from apps.auth_accounts.services.auth_service import AuthService


class AuthView(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

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