from django.apps import AppConfig
from django.db.models.signals import post_save


class FeedsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feeds"

    def ready(self):
        from . import signals
        from .models import Status

        post_save.connect(signals.schedule_status_deletion, sender=Status)
