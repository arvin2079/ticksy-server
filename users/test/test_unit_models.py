from django.test import TestCase
from users.models import User, Identity, UNIDENTIFIED, \
    user_avatar_directory_path, user_identifier_image_directory_path


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

    def test_user_str_1(self):
        sample_user = User.objects.create_user(
            email='sample@test.test',
            password='123456',
            first_name='amirali',
            last_name='sabouri'
        )
        self.assertEqual(str(sample_user), sample_user.first_name + " " + sample_user.last_name)

    def test_user_str_2(self):
        sample_user = User.objects.create_user(
            email='sample@test.test',
            password='123456',
        )
        self.assertEqual(str(sample_user), sample_user.email)

    def test_identity_str(self):
        sample_user = User.objects.create_user(
            email='sample@test.test',
            password='123456',
        )
        sample_user_identity = sample_user.identity
        self.assertEqual(str(sample_user_identity), str(sample_user) + ' ' + sample_user_identity.status)

    def test_user_isactive_by_default(self):
        self.assertTrue(self.user.is_active)

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

    def test_user_avatar_directory_path(self):
        sample_user = User.objects.create_superuser(
            email='sample@test.test',
            password='123456',
        )
        sample_filename = 'avatar.jpg'

        expected = 'user/sample/avatar/avatar.jpg'

        self.assertEqual(user_avatar_directory_path(sample_user, sample_filename), expected)

    def test_user_identifier_image_directory_path(self):
        sample_user = User.objects.create_superuser(
            email='sample@test.test',
            password='123456',
        )
        sample_identity = sample_user.identity
        sample_filename = 'identifier.jpg'

        expected = 'user/sample/identifier-image/identifier.jpg'

        self.assertEqual(user_identifier_image_directory_path(sample_identity, sample_filename), expected)


    def test_identity_assign_to_user(self):
        identity = Identity.objects.get(user=self.user)
        self.assertEqual(identity.user, self.user)

    def test_identity_status(self):
        identity = Identity.objects.get(user=self.user)
        self.assertEqual(identity.status, UNIDENTIFIED)
