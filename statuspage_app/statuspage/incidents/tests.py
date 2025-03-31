from django.test import TestCase
from incidents.models import Incident

class IncidentTestCase(TestCase):
    def test_create_incident(self):
        incident = Incident.objects.create(title="Test Outage", status="investigating")
        self.assertEqual(incident.status, "investigating")
