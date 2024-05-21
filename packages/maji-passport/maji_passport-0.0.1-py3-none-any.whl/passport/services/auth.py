import datetime

import jwt
from countries_plus.models import Country
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.conf import settings
from jwt import InvalidAlgorithmError, ExpiredSignatureError
from loguru import logger

from argo.passport.models import PassportUser, AccessToken, TargetAccess

User = get_user_model()


class RSAManager:
    _instance = None
    file_data = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RSAManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def read_file(self, file_path):
        with open(file_path, "r") as file:
            self.file_data = file.read()

    def get_file_data(self):
        return self.file_data


rsa_manager = RSAManager()
rsa_manager.read_file(settings.PASSPORT_PUBLIC_KEY_PATH)


class RSAPassportService:
    def __init__(
        self,
        iat,
        exp,
        email,
        user_uuid,
        user_auth_code,
        username,
        country_iso,
        access_token,
    ):
        self.email = email
        self.passport_uuid = user_uuid
        self.user_auth_code = user_auth_code
        self.username = username
        self.country_iso = country_iso
        self.access_token = access_token
        self.iat = iat
        self.exp = exp

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

    def _prepare_passport(self, user) -> PassportUser:
        try:
            passport = PassportUser.objects.get(argo_user_id=user.id)
        except ObjectDoesNotExist:
            passport = PassportUser(
                argo_user_id=user.id,
                user_auth_code=self.user_auth_code,
                passport_uuid=self.passport_uuid,
            )
            passport.save()
        return passport

    def _prepare_access_token(self, passport: PassportUser) -> AccessToken:
        try:
            access_token_obj = AccessToken.objects.get(
                passport_user=passport, target=TargetAccess.MAIN
            )
            access_token_obj.token = self.access_token
            access_token_obj.token_expiration = datetime.datetime.utcfromtimestamp(
                self.exp
            )
            access_token_obj.save()
        except ObjectDoesNotExist:
            access_token_obj = AccessToken.objects.create(
                passport_user=passport,
                target=TargetAccess.MAIN,
                token=self.access_token,
                token_expiration=self.exp,
            )
            logger.info(
                f"Create AccessToken object for " f"the user {passport.passport_uuid}"
            )
        return access_token_obj

    def prepare_user(self):
        try:
            user = User.objects.get(email=self.email)
        except ObjectDoesNotExist:
            user = self._create_user()
            logger.info(
                f"User with email doesn't exist: {self.email}, "
                f"created new - {user.uuid}"
            )
        logger.info(f"Start exchange process for user {user.uuid}")
        passport = self._prepare_passport(user)
        logger.info(f"Get passport for user {user.uuid}")
        access_token_obj = self._prepare_access_token(passport)

        return user, access_token_obj

    @staticmethod
    def parse_token(token) -> dict:
        rsa_manager = RSAManager()
        public_key = rsa_manager.get_file_data()
        try:
            decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        except InvalidAlgorithmError as e:
            logger.warning(f"Can't decode token: {token}")
            raise InvalidAlgorithmError(e)
        except ExpiredSignatureError as e:
            raise ExpiredSignatureError(e)

        return decoded
