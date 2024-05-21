from typing import List

from django.contrib.auth import get_user_model
from django.db.models import Q

from argo.passport.services.passport_migrate import PassportMigrateService
from config import celery_app

User = get_user_model()


@celery_app.task
def migrate_users_to_passport_task(ids: List[int]):
    """
    Collect selected registered and not migrated users data and send it to passport
    """
    users = (
        User.objects.filter(id__in=ids)
        .exclude(
            Q(email="") |
            Q(email__isnull=True) |
            Q(email__icontains="appleid.com"),
        )
        .distinct("email")
        .values("username", "email", "phone", "is_phone_verified", "is_email_verified")
    )

    data_list = [
        dict(
            username=user.get("username"),
            email=user.get("email"),
            phone=str(user.get("phone", "")),
            is_email_verified=user.get("is_email_verified"),
            is_phone_verified=user.get("is_phone_verified"),
        )
        for user in users
    ]

    PassportMigrateService.send_users_data(data_list)


@celery_app.task
def migrate_all_users_to_passport_task():
    """
    Collect all registered and not migrated users data and send it to passport
    """
    users = (
        User.objects.filter(
            is_active=True,
            registered_at__isnull=False,
            deleted_dt__isnull=True,
            extra__migrated_to_passport=False,
        )
        .exclude(
            Q(email="") |
            Q(email__isnull=True) |
            Q(email__icontains="appleid.com"),
        )
        .distinct("email")
        .values("username", "email", "phone", "is_phone_verified", "is_email_verified")
    )

    data_list = [
        dict(
            username=user.get("username"),
            email=user.get("email"),
            phone=str(user.get("phone", "")),
            is_email_verified=user.get("is_email_verified"),
            is_phone_verified=user.get("is_phone_verified"),
        )
        for user in users
    ]

    PassportMigrateService.send_users_data(data_list)


@celery_app.task
def migrate_user_password_to_passport_task(email: str, password: str):
    PassportMigrateService.migrate_password(email=email, password=password)
