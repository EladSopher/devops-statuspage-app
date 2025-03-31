from django.test import TestCase
from sp_external_status_providers.models import ExternalStatusPage

class ExternalStatusProviderTestCase(TestCase):
    def test_create_external_page(self):
        page = ExternalStatusPage.objects.create(name="AWS", url="https://status.aws.amazon.com")
        self.assertIn("aws", page.url)
