from django.test import TestCase
from utilities.models import Banner

class UtilitiesTestCase(TestCase):
    def test_create_banner(self):
        banner = Banner.objects.create(message="Maintenance Notice", level="info")
        self.assertIn("Maintenance", banner.message)
