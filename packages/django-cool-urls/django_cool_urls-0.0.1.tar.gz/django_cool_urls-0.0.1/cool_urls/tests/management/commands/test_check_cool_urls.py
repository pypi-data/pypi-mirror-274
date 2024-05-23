from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from ....models import CoolUrl


class CommandTestCase(TestCase):
    MOCK_HTTPX_GET = "cool_urls.management.commands.check_cool_urls.httpx.get"

    def test_everything_is_fine(self):
        # Arrange
        not_ready = CoolUrl.objects.create(
            url="https://example.com/0",
            is_ready=False,
            show_local=False,
        )
        ready_local = CoolUrl.objects.create(
            url="https://example.com/1",
            is_ready=True,
            show_local=True,
            archived_at=timezone.now(),
        )
        ready_remote = CoolUrl.objects.create(
            url="https://example.com/2",
            is_ready=True,
            show_local=False,
            archived_at=timezone.now(),
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=200)
            call_command("check_cool_urls")

        not_ready.refresh_from_db()
        ready_local.refresh_from_db()
        ready_remote.refresh_from_db()

        # Assert
        self.assertFalse(not_ready.is_ready)
        self.assertFalse(not_ready.show_local)

        self.assertTrue(ready_local.is_ready)
        self.assertTrue(ready_local.show_local)

        self.assertTrue(ready_remote.is_ready)
        self.assertFalse(ready_remote.show_local)

    def test_everything_404(self):
        # Arrange
        not_ready = CoolUrl.objects.create(
            url="https://example.com/0",
            is_ready=False,
            show_local=False,
        )
        ready_local = CoolUrl.objects.create(
            url="https://example.com/1",
            is_ready=True,
            show_local=True,
            archived_at=timezone.now(),
        )
        ready_remote = CoolUrl.objects.create(
            url="https://example.com/2",
            is_ready=True,
            show_local=False,
            archived_at=timezone.now(),
        )

        # Act
        with patch(self.MOCK_HTTPX_GET) as m:
            m.return_value = Mock(status_code=404)
            call_command("check_cool_urls")

        not_ready.refresh_from_db()
        ready_local.refresh_from_db()
        ready_remote.refresh_from_db()

        # Assert
        self.assertFalse(not_ready.is_ready)
        self.assertFalse(not_ready.show_local)

        self.assertTrue(ready_local.is_ready)
        self.assertTrue(ready_local.show_local)

        self.assertTrue(ready_remote.is_ready)
        self.assertTrue(ready_remote.show_local)
