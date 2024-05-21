from urllib.parse import urlencode

import httpx
import loguru
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from argo.passport.serializers.exchange import (
    TokenExchangeRequestSerializer,
    ServiceKeySerializer,
    AccessTokenSerializer,
    UpdateUserInfoSerializer,
)
from argo.passport.services.exchange import ExchangeTokenService
from argo.users.models import User


class ExchangeTokenViewSet(GenericViewSet):
    serializer_class = TokenExchangeRequestSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=TokenExchangeRequestSerializer,
        responses={204: Serializer()},
    )
    @action(
        detail=False, methods=["post"], serializer_class=TokenExchangeRequestSerializer
    )
    def exchange(self, request):
        """
        Part of the flow with exchanging tokens.
        This endpoint is used by passport server request. Server-server only.
        Get Information about user and update tokens for him.
        """
        serializer = TokenExchangeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        exchange_service = ExchangeTokenService(**dict(serializer.data))
        exchange_service.exchange()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=AccessTokenSerializer,
        responses={204: Serializer()},
    )
    @action(detail=False, methods=["post"], serializer_class=AccessTokenSerializer)
    def auth_continue_flow(self, request):
        """
        All responsibility for this part of code is on Dmitry and Aleksei
        """
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.data)
        ExchangeTokenService.auto_continue_flow(data["access_token"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["POST"],
    )
    def update_token(self, request):
        """
        Made server-server request for update token
        """
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.data["access_token"]
        params = {
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }
        backwards_url = request.GET.get("backwards_url", None)
        if backwards_url:
            params["backwards_url"] = backwards_url
        response = httpx.post(
            settings.PASSPORT_UPDATE_TOKEN_URL + "?" + urlencode(params),
            headers={"Authorization": f"Bearer {token}"},
            timeout=300,
        )
        return Response(response.json(), status=response.status_code)


class ServiceToken(GenericViewSet):
    @swagger_auto_schema(
        responses={200: ServiceKeySerializer()},
    )
    @action(detail=False, methods=["get"])
    def get_service_key(self, request):
        """
        Get service token for exchange data on OT4 Passport
        """

        return Response(
            status=status.HTTP_200_OK,
            data={"service_key": settings.PASSPORT_SERVICE_KEY},
        )


class UpdateUserInfo(GenericViewSet):
    serializer_class = UpdateUserInfoSerializer
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=["post"],
        serializer_class=UpdateUserInfoSerializer,
    )
    def email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.data)
        old_email = data.get("old_email")
        new_email = data.get("new_email")

        if not new_email:
            raise ValidationError("New email can't be empty")

        try:
            user = User.objects.get(email__iexact=old_email)
            user.email = new_email
            user.is_email_verified = data.get("is_email_verified")
            user.save()

            # add logs
            loguru.logger.info(
                f"User {user.id} update email from {old_email} to {new_email}"
            )
        except User.DoesNotExist:
            raise ValidationError(f"User with email {old_email} does not exist.")
        except User.MultipleObjectsReturned:
            raise ValidationError(f"Returned more than one User with email {old_email}")

        return Response(status=status.HTTP_200_OK)
