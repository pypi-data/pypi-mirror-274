from .models import CoolUrl
from .signals import new_url_created


def relay_creation(sender, instance: CoolUrl, created: bool, **kwargs):
    """
    Yes, we could just tell people to listen to Django's post_save signal, but
    this way, we can change how a CoolUrl gets created in the future and not
    break other people's stuff.
    """
    if created:
        new_url_created.send(sender=instance.__class__, cool_url=instance)
