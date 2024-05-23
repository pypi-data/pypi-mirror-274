import datetime
import re

from django.conf import settings
from jwt import InvalidAlgorithmError, ExpiredSignatureError
from rest_framework.exceptions import AuthenticationFailed

from maji_passport.models import AccessToken
from maji_passport.services.auth import RSAPassportService
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

APPLICATION_AUTHENTICATION = settings.INHERITANCE_AUTHENTICATION if getattr(settings, "APPLICATION_AUTHENTICATION")else JSONWebTokenAuthentication


class CommonPassportBackend(APPLICATION_AUTHENTICATION):
    def check_permission(self, access_token_obj):
        raise NotImplementedError

    def _authenticate_by_passport(self, request):
        """
        New authentication logic here
        Return the user object if authentication is successful, None otherwise"
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, None
        token = re.sub(r"^Bearer\s*", "", token).strip()
        access_token_obj = AccessToken.objects.filter(token=token).first()
        if access_token_obj and access_token_obj.passport_user is not None:
            return self.check_permission(access_token_obj)
        else:
            try:
                payload = RSAPassportService.parse_token(token)
                service = RSAPassportService(**payload, access_token=token)
                return service.prepare_user()
            except InvalidAlgorithmError:
                pass
            except ExpiredSignatureError:
                raise AuthenticationFailed("Token is expired")
            return None, None

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise, returns `None`.
        """

        user = self._authenticate_by_passport(request)
        if user[0]:
            return user

        user = super().authenticate(request)

        return user


class PassportAuthBackend(CommonPassportBackend):
    """
    For passport auth
    """

    def check_permission(self, access_token_obj):
        if access_token_obj.is_token_expired:
            try:
                payload = RSAPassportService.parse_token(access_token_obj.token)
            except InvalidAlgorithmError:
                return None, None
            except ExpiredSignatureError:
                raise AuthenticationFailed("Token is expired")

            cert_exp = datetime.datetime.utcfromtimestamp(payload["exp"])
            if cert_exp < datetime.datetime.now():
                raise AuthenticationFailed("Token is expired")
            else:
                access_token_obj.token_expiration = cert_exp
                access_token_obj.save()
        return access_token_obj.passport_user.argo_user, access_token_obj.token


class PassportExpireTokenBackend(CommonPassportBackend):
    """
    Update token for only seamless flow
    """

    def check_permission(self, access_token_obj):
        pass
