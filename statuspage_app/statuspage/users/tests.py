from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.utils import timezone
from users.models import UserConfig, Token, ObjectPermission
import datetime


class UserConfigTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_userconfig_created_on_user_creation(self):
        self.assertTrue(hasattr(self.user, 'config'))

    def test_set_and_get_preference(self):
        self.user.config.set("ui.theme", "dark", commit=True)
        self.assertEqual(self.user.config.get("ui.theme"), "dark")


class TokenTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apitestuser")

    def test_token_creation_and_expiry(self):
        token = Token.objects.create(user=self.user)
        self.assertIsNotNone(token.key)
        self.assertFalse(token.is_expired)

    def test_token_expired_property(self):
        expired_token = Token.objects.create(user=self.user, expires=timezone.now() - datetime.timedelta(days=1))
        self.assertTrue(expired_token.is_expired)


class ObjectPermissionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="permuser")
        self.group = Group.objects.create(name="permgroup")
        self.content_type = ContentType.objects.get_for_model(User)

    def test_create_object_permission(self):
        perm = ObjectPermission.objects.create(
            name="View Users",
            description="Can view user objects",
            enabled=True,
            actions=["view"]
        )
        perm.users.add(self.user)
        perm.groups.add(self.group)
        perm.object_types.add(self.content_type)

        self.assertIn("view", perm.actions)
        self.assertEqual(perm.__str__(), "View Users")
