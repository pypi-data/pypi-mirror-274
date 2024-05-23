from django import template
from django.conf import settings

from ..models import CoolUrl


register = template.Library()


POLICY = getattr(settings, "COOL_URLS_POLICY", "REMOTE")


@register.simple_tag()
def cool_embed(url: str) -> str:
    """
    Attempts to embed the URL, assuming it's a video of some kind.
    """
    return CoolUrl.objects.get_or_create(
        url=url,
        defaults={
            "show_local": POLICY == "LOCAL",
            "is_embedded": True,
        },
    )[0].markup


@register.simple_tag()
def cool_url(url: str) -> str:
    return CoolUrl.objects.get_or_create(
        url=url,
        defaults={
            "show_local": POLICY == "LOCAL",
        },
    )[0].markup
