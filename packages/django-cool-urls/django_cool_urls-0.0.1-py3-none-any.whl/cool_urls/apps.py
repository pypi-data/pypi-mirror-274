from django.apps import AppConfig
from django.db.models.signals import post_save


class CoolUrlsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cool_urls"
    verbose_name = "Cool URLs"

    def ready(self):
        from .models import CoolUrl
        from .receivers import relay_creation

        post_save.connect(relay_creation, sender=CoolUrl)
