from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, URLField
from rest_framework.serializers import Serializer


class UserPassportSetPasswordSerializer(Serializer):
    password = CharField()

    def validate(self, attrs):
        user = self.context["request"].user
        if user.check_password(attrs["password"]) is False:
            raise ValidationError("Wrong password")
        return attrs


class GetLoginUrlOutputSerializer(Serializer):
    url = URLField()
