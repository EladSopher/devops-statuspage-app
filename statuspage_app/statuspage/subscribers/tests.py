from django.test import TestCase
from subscribers.models import Subscriber

class SubscriberTestCase(TestCase):
    def test_create_subscriber(self):
        subscriber = Subscriber.objects.create(email="test@example.com")
        self.assertIn("@example.com", subscriber.email)
