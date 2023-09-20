from django.apps import AppConfig


class LiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'live'

    def ready(self):
        import live.signals