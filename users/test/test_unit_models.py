from django.test import TestCase
from users.models import User, Identity, REQUESTED, IDENTIFIED, UNIDENTIFIED


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='ab@ab.com',
            password='12345678',
        )

    def test_user_create_successfully(self):
        sample_user = User.objects.create_user(
            email='sample@test.test',
            password='123456',
        )

        self.assertTrue(sample_user.id)

    def test_user_without_email(self):
        self.assertRaises(ValueError, lambda: User.objects.create_user(
            email='',
            password='123456',
        ))

        self.assertRaises(TypeError, lambda: User.objects.create_user(
            password='123456',
        ))

    ## FIXME : thisssssss
    def test_user_invalid_email(self):

        user = User.objects.create_user(
            email='test.com',
            password='123456',
        )

        print(user.email)

        # self.assertRaises(ValueError, lambda: User.objects.create_user(
        #     email='test.com',
        #     password='123456',
        # ))

    def test_user_assign_email_on_creation(self):
        self.assertEqual(self.user.email, 'ab@ab.com')

    def test_user_assign_password_on_creation(self):
        self.assertTrue(self.user.check_password('12345678'))

    def test_user_create_superuser_successfully(self):
        sample_user = User.objects.create_superuser(
            email='sample@test.test',
            password='123456',
        )

        self.assertTrue(sample_user.is_staff)
        self.assertTrue(sample_user.is_superuser)

    def test_identity_assign_to_user(self):
        identity = Identity.objects.get(user=self.user)
        self.assertEqual(identity.user, self.user)

    def test_identity_status(self):
        identity = Identity.objects.get(user=self.user)
        self.assertEqual(identity.status, UNIDENTIFIED)
