from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import HashIndex
from django.db.models import (
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    TextChoices,
    OneToOneField,
    CASCADE,
)
from django.db.models.fields import UUIDField, TextField
from django.utils import timezone

from argo.common.models import BaseModel

User = get_user_model()


class PassportUser(BaseModel):
    argo_user = OneToOneField(User, null=True, on_delete=SET_NULL)
    passport_uuid = UUIDField(null=False)
    user_auth_code = CharField(max_length=255, null=False)
    refresh_token = TextField()

    def __str__(self):
        return (
            f"argo email - {self.argo_user.email}, passport uuid - {self.passport_uuid}"
        )


class TargetAccess(TextChoices):
    MAIN = "main", "Main"
    Android = "android", "Android"
    ROKU = "roku", "Roku"
    EXTRA = "extra", "Extra"


class AccessToken(BaseModel):
    class Meta:
        indexes = (HashIndex(fields=("token",)),)

    passport_user = ForeignKey(PassportUser, null=True, on_delete=CASCADE)
    token = TextField()
    token_expiration = DateTimeField(auto_now_add=True)
    target = CharField(
        max_length=30, choices=TargetAccess.choices, default=TargetAccess.MAIN
    )

    def __str__(self):
        return f"Access token for: {self.passport_user}"

    @property
    def is_token_expired(self) -> bool:
        return self.token_expiration < timezone.now()
