from datetime import datetime

from django.test import TestCase

from user.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password='<PASSWORD>',
            email='admon@admon.com',
            birthday=datetime(1999, 12, 25),
        )

    def test_user_birthday(self):
        self.assertEqual(self.user.time_to_string, "Рік: 99, 25 грудня")
