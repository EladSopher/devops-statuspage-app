from django.test import TestCase
from components.models import Component

class ComponentModelTest(TestCase):
    def test_create_component(self):
        component = Component.objects.create(
            name="API Server",
            status="operational"
        )
        self.assertEqual(component.name, "API Server")
        self.assertEqual(component.status, "operational")
