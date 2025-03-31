from django.test import TestCase
from extras.models import ConfigContext

class ExtrasTestCase(TestCase):
    def test_create_config_context(self):
        context = ConfigContext.objects.create(name="Test Context", weight=10)
        self.assertEqual(context.name, "Test Context")
