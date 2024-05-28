from datetime import datetime

from django.test import TestCase

from user.forms import UserCreateForm


class FormTests(TestCase):
    def test_user_create_form_valid(self):
        form_data = {
            'email': 'email1@email.com',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'birthday': datetime(1990, 1, 1),
            'number': 123123121212,
            'card': 1111111111111112,
            'password1': 'PASSWORd123',
            'password2': 'PASSWORd123',
        }
        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
