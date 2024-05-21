from django.core.management import BaseCommand

from argo.passport.tasks import migrate_all_users_to_passport_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        migrate_all_users_to_passport_task.delay()
