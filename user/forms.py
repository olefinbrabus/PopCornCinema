from user.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', "birthday", "number", 'email', "password1", "password2",)


class UserChangedForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', "birthday", "number", 'email', "card",)


class UserPasswordChangedForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ("new_password1", "new_password2")
