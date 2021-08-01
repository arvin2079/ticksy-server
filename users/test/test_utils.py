from ..utils import ActivationEmailTokenGenerator
from ..models import User
from django.test import TestCase


class TestUtils(TestCase):

    def test_ActivationEmailTokenGenerator_1(self):
        token_gen = ActivationEmailTokenGenerator()
        user = User.objects.create_user(
            'first@example.com',
            '123456',
        )

        token = token_gen.make_token(user)
        self.assertTrue(token_gen.check_token(user, token))

    def test_ActivationEmailTokenGenerator_2(self):
        token_gen = ActivationEmailTokenGenerator()
        first_user = User.objects.create_user(
            'first@example.com',
            '123456',
        )

        second_user = User.objects.create_user(
            'second@example.com',
            '123456',
        )

        token = token_gen.make_token(first_user)
        self.assertFalse(token_gen.check_token(second_user, token))
