from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.fields import BooleanField, CharField

from rest_framework.serializers import Serializer

from utils import clear_phone_number

User = get_user_model()

USER_DETAIL_SERIALIZER = settings.USER_DETAIL_SERIALIZER if settings.get("USER_DETAIL_SERIALIZER") else Serializer


class KafkaUpdateUserSerializer(USER_DETAIL_SERIALIZER):
    """
    Serializer for kafka update user messages

    phone and is_phone_verified is read_only_fields in ArgoUserDetailsSerializer
    and here we must declare them read_only=False and required=False
    """
    phone = CharField(read_only=False, required=False, allow_blank=True)
    is_phone_verified = BooleanField(read_only=False, required=False)

    def validate_phone(self, value):
        return clear_phone_number(value)

    def update(self, instance, validated_data):
        """
        If we get a phone number in data, this means that the user has changed phone
        in the passport and needs to update it for the current user
        and remove it from other users, who have that phone
        """
        if "phone" in validated_data and validated_data["phone"]:
            old_users = User.objects.filter(phone=validated_data["phone"])
            old_users.update(phone="", is_phone_verified=False)
        # update avatar from kafka.
        # otherwise rise errors:
        # - ValueError: Cannot assign "3743": "User.avatar" must be a "Image" instance
        # - Incorrect type. Expected pk value, received Image.
        # if "avatar" in validated_data and validated_data["avatar"]:
        #     avatar_id = validated_data.pop("avatar")
        #     avatar = Image.objects.get(id=avatar_id)
        #     instance.avatar = avatar
        return super().update(instance, validated_data)
