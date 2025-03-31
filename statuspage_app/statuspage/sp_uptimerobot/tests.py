from django.test import TestCase
from sp_uptimerobot.models import UptimeRobotMonitor

class UptimeRobotTestCase(TestCase):
    def test_create_monitor(self):
        monitor = UptimeRobotMonitor.objects.create(name="Google", url="https://www.google.com")
        self.assertTrue(monitor.url.startswith("https://"))
