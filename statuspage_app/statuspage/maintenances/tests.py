from django.test import TestCase
from maintenances.models import Maintenance

class MaintenanceTestCase(TestCase):
    def test_schedule_maintenance(self):
        m = Maintenance.objects.create(title="DB Upgrade", status="scheduled")
        self.assertEqual(m.title, "DB Upgrade")
