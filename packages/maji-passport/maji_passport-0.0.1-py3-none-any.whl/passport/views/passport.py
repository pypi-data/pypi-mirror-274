import datetime
from urllib.parse import urlencode

from django.conf import settings
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from argo.passport.authentication.backend import (
    PassportExpireTokenBackend,
)
from argo.passport.serializers.exchange import AccessTokenSerializer
from argo.passport.serializers.passport import (
    UserPassportSetPasswordSerializer,
    GetLoginUrlOutputSerializer,
)
from argo.passport.services.exchange import ExchangeTokenService
from argo.users.models import User
from argo.passport.services.passport_migrate import PassportMigrateService


class UserPassportViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        serializer_class=UserPassportSetPasswordSerializer,
    )
    def migrate_password(self, request):
        """
        Migrate user password to passport profile
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        passport_response = PassportMigrateService.migrate_password(
            email=user.email,
            password=serializer.data["password"],
        )

        return Response(passport_response.json(), status=passport_response.status_code)

    @swagger_auto_schema(
        request_body=Serializer,
        responses={204: Serializer()},
    )
    @action(
        detail=False,
        methods=["POST"],
    )
    def set_tokens_expired(self, request):
        """
        Expired user token
        """

        access_token = request.user.passportuser.accesstoken_set.filter(
            target="main"
        ).first()
        access_token.token_expiration = timezone.now() - datetime.timedelta(hours=10)
        access_token.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PassportViewSet(GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = GetLoginUrlOutputSerializer

    @action(
        detail=False,
        methods=["GET"],
    )
    def get_login_url(self, request):
        """
        Get url for passport login
        """
        params = {
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }
        backwards_url = request.GET.get("backwards_url", None)
        if backwards_url:
            params["backwards_url"] = backwards_url

        serializer = self.serializer_class(
            {"url": settings.PASSPORT_LOGIN_URL + "?" + urlencode(params)}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpiredPassportViewSet(GenericViewSet):
    serializer_class = AccessTokenSerializer
    authentication_classes = [PassportExpireTokenBackend]

    @swagger_auto_schema(
        request_body=Serializer, responses={200: AccessTokenSerializer()}
    )
    @action(
        detail=False,
        methods=["POST"],
    )
    def update_token(self, request):
        """
        Deprecated. We don't use refresh token with Passport v2

        Update token by expired ones.
        """
        access_token_obj = request.user.passportuser.accesstoken_set.filter(
            target="main"
        ).first()
        access_token = ExchangeTokenService.update_token_by_refresh(access_token_obj)
        serializer = self.serializer_class({"access_token": access_token})
        return Response(serializer.data, status=status.HTTP_200_OK)
