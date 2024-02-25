from django import forms
from user.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',"birthday","number", 'email']

