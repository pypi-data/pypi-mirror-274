from unittest.mock import patch

from django.test import TestCase

from ..models import CoolUrl
from ..templatetags.cool_urls import cool_embed, cool_url


class CoolEmbedTestCase(TestCase):
    def test_without_policy(self):
        url = "https://youtube.com/watch?v=test"
        cool_embed(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertFalse(cu.show_local)
        self.assertTrue(cu.is_embedded)

    @patch("cool_urls.templatetags.cool_urls.POLICY", "LOCAL")
    def test_with_policy(self):
        url = "https://youtube.com/watch?v=test"
        cool_embed(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertTrue(cu.show_local)
        self.assertTrue(cu.is_embedded)

    def test_multiple_invocations(self):
        url = "https://youtube.com/watch?v=test"
        cool_embed(url)
        cool_embed(url)
        self.assertEqual(CoolUrl.objects.count(), 1)


class CoolUrlTestCase(TestCase):
    def test_without_policy(self):
        url = "https://example.com/"
        cool_url(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertFalse(cu.show_local)
        self.assertFalse(cu.is_embedded)

    @patch("cool_urls.templatetags.cool_urls.POLICY", "LOCAL")
    def test_with_policy(self):
        url = "https://example.com/"
        cool_url(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
        cu = CoolUrl.objects.get(url=url)
        self.assertEqual(cu.url, url)
        self.assertTrue(cu.show_local)
        self.assertFalse(cu.is_embedded)

    def test_multiple_invocations(self):
        url = "https://example.com/"
        cool_url(url)
        cool_url(url)
        self.assertEqual(CoolUrl.objects.count(), 1)
