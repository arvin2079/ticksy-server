from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.api.views import UserInfoApiView, SigninApiView, SignupApiView, ActivateEmail, IdentityApiView, \
    ResetPasswordRequest, ResetPasswordValidateToken, ResetPasswordNewPassword


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
