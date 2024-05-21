import httpx
from countries_plus.models import Country
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from loguru import logger
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from argo.passport.serializers.exchange import (
    TokenExchangeResponseSerializer,
    TokenExchangeCompleteSerializer,
    FullAccessTokenSerializer,
)
from argo.passport.models import PassportUser, AccessToken, TargetAccess

User = get_user_model()


class ExchangeTokenService:
    def __init__(self, email, user_uuid, user_auth_code, username, country_iso):
        self.email = email
        self.passport_uuid = user_uuid
        self.user_auth_code = user_auth_code
        self.username = username
        self.country_iso = country_iso

    @staticmethod
    def _send_post_request(url, data):
        response = httpx.post(url, json=data, timeout=120)
        return response.json()

    def _create_user(self):
        try:
            country = Country.objects.get(iso=self.country_iso)
            user = User.objects.create(
                email=self.email,
                username=self.username,
                display_name=self.username,
                country_on_create=country,
            )
            user.register_and_save()
            user.extra["migrated_to_passport"] = True
            user.save()
        except IntegrityError:
            user = User.objects.get(email=self.email)
            if not user.display_name:
                user.display_name = self.username
            user.extra["migrated_to_passport"] = True
            user.save()

        return user

    def _get_and_validate_passport(self, user) -> PassportUser:
        try:
            passport = PassportUser.objects.get(argo_user_id=user.id)
        except ObjectDoesNotExist:
            passport = PassportUser(
                argo_user_id=user.id,
                user_auth_code=self.user_auth_code,
                passport_uuid=self.passport_uuid,
            )
            passport.save()
        else:
            if (
                str(passport.passport_uuid) != self.passport_uuid
                or passport.user_auth_code != self.user_auth_code
            ):
                raise AuthenticationFailed(
                    "Missmatch credentials: "
                    f"passport uuid ={passport.passport_uuid}, "
                    f"auth_code = {passport.user_auth_code}, "
                    f"self uuid = {self.passport_uuid}, "
                    f"auth_code = {self.user_auth_code}"
                )
        return passport

    def _get_access_token_by_passport(self, passport: PassportUser) -> AccessToken:
        try:
            access_token_obj = AccessToken.objects.get(
                passport_user=passport, target=TargetAccess.MAIN
            )
        except ObjectDoesNotExist:
            access_token_obj = AccessToken.objects.create(
                passport_user=passport, target=TargetAccess.MAIN
            )
            logger.info(
                f"Create AccessToken object for " f"the user {passport.passport_uuid}"
            )
        return access_token_obj

    def request_for_tokens(self) -> dict:
        data = {
            "user_uuid": self.passport_uuid,
            "user_auth_code": self.user_auth_code,
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }
        serializer = TokenExchangeResponseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        response_dict = self._send_post_request(settings.PASSPORT_EXCHANGE_URL, data)

        serializer = TokenExchangeCompleteSerializer(data=response_dict)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def exchange(self):
        try:
            user = User.objects.get(email=self.email)
        except ObjectDoesNotExist:
            user = self._create_user()
            logger.info(
                f"User with email doesn't exist: {self.email}, "
                f"created new - {user.uuid}"
            )
        logger.info(f"Start exchange process for user {user.uuid}")
        passport = self._get_and_validate_passport(user)
        logger.info(f"Get passport for user {user.uuid}")
        tokens = self.request_for_tokens()
        logger.info(f"Get tokens for user {user.uuid}")
        access_token_obj = self._get_access_token_by_passport(passport)

        self.save_tokens(access_token_obj, tokens)
        return True

    @staticmethod
    def save_tokens(access_token_obj: AccessToken, tokens: dict):
        logger.info(
            f"Token was updated for passport "
            f"{access_token_obj.passport_user.passport_uuid}"
        )
        access_token_obj.token = tokens["access_token"]
        access_token_obj.token_expiration = tokens["access_token_expiration"]
        if tokens.get("refresh_token"):
            access_token_obj.passport_user.refresh_token = tokens["refresh_token"]
        access_token_obj.save()
        access_token_obj.passport_user.save()
        logger.info(
            f"Token was updated "
            f"for passport {access_token_obj.passport_user.passport_uuid}"
        )

    @classmethod
    def update_token_by_refresh(cls, access_token_obj: AccessToken) -> str:
        data = {
            "refresh_token": access_token_obj.passport_user.refresh_token,
            "service_key": settings.PASSPORT_SERVICE_KEY,
        }
        logger.info(
            f"Start update token process for user "
            f"{access_token_obj.passport_user.argo_user.uuid}"
        )

        response_dict = cls._send_post_request(
            settings.PASSPORT_ACCESS_BY_REFRESH_URL, data
        )

        serializer = FullAccessTokenSerializer(data=response_dict)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        logger.info(
            f"Get new tokens for user "
            f"{access_token_obj.passport_user.argo_user.uuid}"
        )

        cls.save_tokens(access_token_obj, data)
        logger.info(
            f"Save tokens for user " f"{access_token_obj.passport_user.argo_user.uuid}"
        )
        return data["access_token"]

    @staticmethod
    def auto_continue_flow(external_token):
        continue_url = (
            f"{settings.PASSPORT_CONTINUE_URL}?"
            f"service_key={settings.PASSPORT_SERVICE_KEY}"
        )
        response = httpx.post(
            continue_url,
            headers={"Authorization": f"Bearer {external_token}"},
            timeout=300,
        )
        if response.status_code != status.HTTP_200_OK:
            raise PermissionDenied("Token is invalid")
        response = response.json()
        new_access_token = response["access_token"]
        argo_token_obj = AccessToken.objects.get(token=new_access_token)

        argo_token_obj.token = external_token
        argo_token_obj.save()
