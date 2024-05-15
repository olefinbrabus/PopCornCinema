from django import forms

from cinema.models import Genre, Ticket, Movie


class MoviesSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Пошук фільма",
                "class": "movie-list-input",
            },
        )
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label='Жанр',
        empty_label='Оберіть жанр',
        widget=forms.Select(
            attrs={
                "class": "movie-list-margin",
            }
        )
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label='В театрі:',
        widget=forms.CheckboxInput(
            attrs={
                "class": "movie-list-margin",
            }
        )
    )

