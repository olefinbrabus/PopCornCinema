from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from user.models import User


USER_ACCOUNT = reverse('user:user-account-detail', args=[1])


class PublicUserTests(TestCase):

    def test_login_required(self):
        response = self.client.get(USER_ACCOUNT)
        self.assertNotEqual(response.status_code, 200)


class PrivateUserTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='email@localshost.com',
            password='<PASSWORD>',
        )
        self.client.force_login(self.user)

    def test_retrieve_user(self):
        response = self.client.get(USER_ACCOUNT)
        self.assertEqual(response.status_code, 200)
