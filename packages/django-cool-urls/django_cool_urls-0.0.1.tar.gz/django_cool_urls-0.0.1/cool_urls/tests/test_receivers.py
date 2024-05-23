from unittest.mock import patch

from django.test import TestCase

from ..models import CoolUrl


class ReceiverTestCase(TestCase):
    @patch("cool_urls.receivers.new_url_created.send")
    def test_signal_triggered_only_on_save(self, m):
        cu = CoolUrl.objects.create(url="https://example.com/")
        cu.save()
        self.assertEqual(m.call_count, 1)
