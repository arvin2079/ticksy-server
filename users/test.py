from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from users.api.views import UserInfoApiView, SigninApiView, SignupApiView, ActivateEmail, IdentityApiView, \
    ResetPasswordRequest, ResetPasswordValidateToken, ResetPasswordNewPassword
from users.models import User, Identity


class TestUrls(SimpleTestCase):

    def test_user_info_url_is_resolved(self):
        url = reverse('users:user_info')
        self.assertEqual(resolve(url).func.view_class, UserInfoApiView)

    def test_user_signin_url_is_resolved(self):
        url = reverse('users:user_signin')
        self.assertEqual(resolve(url).func.view_class, SigninApiView)

    def test_user_signup_url_is_resolved(self):
        url = reverse('users:user_signup')
        self.assertEqual(resolve(url).func.view_class, SignupApiView)

    def test_email_activation_url_is_resolved(self):
        url = reverse('users:email_activation', args=['some-slug', 'some-slug-2'])
        self.assertEqual(resolve(url).func.view_class, ActivateEmail)

    def test_user_identity_url_is_resolved(self):
        url = reverse('users:user_identity')
        self.assertEqual(resolve(url).func.view_class, IdentityApiView)

    def test_reset_password_request_url_is_resolved(self):
        url = reverse('users:reset_password_request')
        self.assertEqual(resolve(url).func.view_class, ResetPasswordRequest)

    def test_reset_password_confirm_credential_url_is_resolved(self):
        url = reverse('users:reset_password_confirm_credential', args=['some-slug', 'some-slug-2'])
        self.assertEqual(resolve(url).func.view_class, ResetPasswordValidateToken)

    def test_reset_password_new_password_url_is_resolved(self):
        url = reverse('users:reset_password_new_password')
        self.assertEqual(resolve(url).func.view_class, ResetPasswordNewPassword)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            email='a@a.com',
            password='12345678',
        )

    def test_UserInfoApiView(self):
        user = User.objects.first()
        self.client.force_login(user=user)
        url = reverse('users:user_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_SigninApiView(self):
        url = reverse('users:user_signin')
        response = self.client.post(url, {
            "username": "a@a.com",
            "password": "12345678"
        })
        self.assertEqual(response.status_code, 200)

    # def test_SignupApiView(self):
    #     url = reverse('users:user_signup')
    #     response = self.client.post(url, {
    #         "email": "u@example.com",
    #         "password": "12345678",
    #         "first_name": "علیرضا",
    #         "last_name": "بیگی"
    #     })
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_ResetPasswordRequest(self):
    #     pass
    #
    # def test_ResetPasswordValidateToken(self):
    #     pass
    #
    # def test_ResetPasswordNewPassword(self):
    #     pass


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
