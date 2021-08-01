from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, IDENTIFIED


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            email='exmaple@example.com',
            password='12345678',
        )

    def test_UserInfoApiView_200(self):
        user = User.objects.first()
        self.client.force_login(user=user)

        url = reverse('users:user_info')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_UserInfoApiView_401(self):
        url = reverse('users:user_info')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_SigninApiView_200(self):
        url = reverse('users:user_signin')
        response = self.client.post(url, {
            "username": "exmaple@example.com",
            "password": "12345678"
        })
        self.assertEqual(response.status_code, 200)

    def test_SigninApiView_400_1(self):
        url = reverse('users:user_signin')
        body = {
            "username": "aa.com",
            "password": "12345678"
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400)

        body['username'] = 'a@a.com'
        body['password'] = '123'

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400)

    def test_SigninApiView_400_2(self):
        url = reverse('users:user_signin')
        body = {
            "username": "a@a.com",
            "password": "123"
        }

        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400)

    def test_SignupApiView_201(self):
        url = reverse('users:user_signup')
        response = self.client.post(url, {
            "email": "us@example.com",
            "password": "12345678",
            "first_name": "علیرضا",
            "last_name": "بیگی"
        })
        self.assertEqual(response.status_code, 201)

    def test_SignupApiView_400(self):
        url = reverse('users:user_signup')
        response = self.client.post(url, {
            "email": "a@a.com",
            "password": "12345678",
            "first_name": "علیرضا",
            "last_name": "بیگی"
        })
        self.assertEqual(response.status_code, 400)

    def test_ResetPasswordRequest_200(self):
        url = reverse('users:reset_password_request')
        response = self.client.post(url, {
            "email": "exmaple@example.com",
        })
        self.assertEqual(response.status_code, 200)

    def test_ResetPasswordRequest_400(self):
        url = reverse('users:reset_password_request')
        response = self.client.post(url, {
            "email": "false@example.com",
        })
        self.assertEqual(response.status_code, 400)

    def test_IdentityApiView_200_1(self):
        user = User.objects.first()
        self.client.force_login(user=user)

        url = reverse('users:user_identity')
        response = self.client.patch(url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_IdentityApiView_401(self):
        url = reverse('users:user_identity')
        response = self.client.patch(url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_IdentityApiView_200_2(self):
        user = User.objects.first()
        self.client.force_login(user=user)
        user.identity.status = IDENTIFIED
        user.save()

        url = reverse('users:user_identity')
        response = self.client.patch(url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
