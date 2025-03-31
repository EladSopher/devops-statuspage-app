from django.test import TestCase
from queuing.models import QueuedTask

class QueuingTestCase(TestCase):
    def test_enqueue_task(self):
        task = QueuedTask.objects.create(name="Test Task", status="pending")
        self.assertEqual(task.status, "pending")
