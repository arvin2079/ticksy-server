from django.test import TestCase, Client
from django.urls import reverse
from users.models import User


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
