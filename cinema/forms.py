from django import forms

from cinema.models import Genre, Ticket
from user.models import User
from django.contrib.auth.forms import UserCreationForm





class MoviesSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Пошук фільма",

            },

        )
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label='Жанр',
        empty_label='Оберіть жанр',
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label='В театрі:',
    )


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['movie_session', 'row', 'seat',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)