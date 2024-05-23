from django.core.management.base import BaseCommand

import httpx

from ...logging import Loggable
from ...models import CoolUrl


class Command(Loggable, BaseCommand):
    """
    Go through all CoolUrl entries and check if the site is still responding
    properly.  If not, set `show_local` to `True` so we prefer the local copy.

    This is the sort of thing you'd probably want to run in a weekly cron or
    something.
    """

    def handle(self, *args, **options):
        urls = CoolUrl.objects.filter(is_ready=True, show_local=False)
        for cool_url in urls.iterator():
            code = httpx.get(cool_url.url).status_code
            if code != httpx.codes.OK:
                self.logger.info(
                    "URL %s had an HTTP response of %s, so we're marking "
                    "it to render the local archived copy.",
                    cool_url.url,
                    code,
                )
                cool_url.show_local = True
                cool_url.save(update_fields=("show_local",))
