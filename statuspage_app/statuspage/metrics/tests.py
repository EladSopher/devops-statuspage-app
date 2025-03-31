from django.test import TestCase
from metrics.models import Metric

class MetricsTestCase(TestCase):
    def test_create_metric(self):
        metric = Metric.objects.create(name="Uptime", current_value=99.9)
        self.assertEqual(metric.name, "Uptime")
