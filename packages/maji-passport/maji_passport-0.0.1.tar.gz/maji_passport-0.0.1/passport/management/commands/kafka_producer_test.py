import json
import os
import sys

from django.core.management.base import BaseCommand

from argo.passport.services.kafka import KafkaService


class Command(BaseCommand):
    help = "Execute test command to produce message to consumer"

    def handle(self, *args, **options):
        """
        Command for test run producer. This part must be on internal service side
        """
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

        service = KafkaService()
        message = {
            "action": "logout",
            "user_auth_code": "c7b1a7b1a89f192004f12aec05551a29",
            "description": "test_description",
            "service_key": "yt90YT9jkBP1PPzySTmzwA",
        }
        service.produce_message(json.dumps(message))
