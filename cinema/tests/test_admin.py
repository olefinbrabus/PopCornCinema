from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client


class CinemaModelsAdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin1@admin.com",
            password="<PASSWORD>",
            birthday=datetime(1998, 1, 2),
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user1@user.com",
            password="<PASSWORD>",
            birthday=datetime(1998, 1, 1),
        )

    def test_user_birthday_listed(self):
        """
        Test that user birthday is listed in admin page
        :return:
        """
        url = reverse("admin:user_user_changelist")
        response = self.client.get(url)
        self.assertContains(response, "1998")

    def test_user_detail_birthday_listed(self):
        """
        Test that user birthday is listed in detail admin page
        :return:
        """
        url = reverse("admin:user_user_change", args=[self.user.id])
        response = self.client.get(url)
        self.assertContains(response, "1998")

