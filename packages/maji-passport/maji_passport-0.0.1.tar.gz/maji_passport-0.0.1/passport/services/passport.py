import datetime

from argo.passport.models import PassportUser, AccessToken


class PassportService:
    def __init__(self, passport: PassportUser):
        self.passport = passport

    def invalidate_access_tokens(self) -> None:
        self.passport.accesstoken_set.update(token_expiration=datetime.datetime.now())
