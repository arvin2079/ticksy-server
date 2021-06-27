from django.test import TestCase
from users.models import User, Identity


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='ab@ab.com',
            password='12345678',
        )
        self.identity = Identity.objects.first()
        self.identity.user = self.user
        self.identity.save()

    def test_user_assign_email_on_creation(self):
        self.assertEqual(self.user.email, 'ab@ab.com')

    def test_user_assign_password_on_creation(self):
        self.assertTrue(self.user.check_password('12345678'))

    def test_identity_assign_to_user(self):
        self.assertEqual(self.identity.user, self.user)
