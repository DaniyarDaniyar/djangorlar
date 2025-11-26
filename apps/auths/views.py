#Python modules
from typing import Any
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import OpenApiResponse, extend_schema

#Django REST Framework modules
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

#Project modules
from django.contrib.auth.models import User
from apps.auths.serializers import UserLoginSerializer, UserLoginResponseSerializer, UserLoginResponseSerializer, UserLoginErrorsSerializer, HTTP405MethodNotAllowedSerializer

class AuthViewSet(ViewSet):
    """
    A viewset for handling authentication-related actions.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Login",
        description="Authenticate a user and return JWT tokens.",
        request=UserLoginSerializer,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successful login",
                response=UserLoginResponseSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request (e.g., invalid credentials)",
                response=UserLoginErrorsSerializer,
            ),
            HTTP_405_METHOD_NOT_ALLOWED: OpenApiResponse(
                description="Method not allowed",
                response=HTTP405MethodNotAllowedSerializer,
            ),
        }
    )
    @action(
        methods=['post'],
        detail=False,
        url_path='login',
        url_name='login',
        permission_classes=[AllowAny],
    )
    def login(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Handle user login and return JWT tokens.
        """

        serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user: User = serializer.validated_data.pop('user')

        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh.access_token)

        return Response(
            data={
                'access': access_token,
                'refresh': str(refresh),
            },
            status=HTTP_200_OK,
        )
