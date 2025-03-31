from django.test import TestCase
from components.models import Component

class ComponentTestCase(TestCase):
    def test_create_component(self):
        component = Component.objects.create(name="API", status="operational")
        self.assertEqual(component.status, "operational")
