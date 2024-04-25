
from django.views import generic

from cinema.forms import *
from cinema.models import *


class IndexView(generic.ListView):
    template_name = "cinema/index.html"
    queryset = Movie.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        main_movie = Movie.objects.get(pk=4)
        context['main_movie'] = main_movie

        return context


class MoviesListView(generic.ListView):
    template_name = "cinema/movie_list.html"
    model = Movie
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(MoviesListView, self).get_context_data(**kwargs)
        context['search_form'] = MoviesSearchForm(data=self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')

        genre_id = self.request.GET.get('genre')
        is_active = self.request.GET.get('is_active')

        conditions = {}

        if title:
            conditions['title'] = title

        if genre_id:
            conditions['genres'] = genre_id

        if is_active:
            conditions['is_active'] = is_active.lower() != 'true'

        self.request.session['search_params'] = {
            'genre': genre_id,
            'is_active': is_active,
        }

        return queryset.filter(**conditions)


class MoviesDetailView(generic.DetailView):
    template_name = "cinema/movie_detail.html"
    model = Movie


class CinemaView(generic.ListView):
    template_name = "cinema/about.html"
    model = CinemaHall


class MovieSessionDetailView(generic.DetailView):
    template_name = 'cinema/movie_session_detail.html'
    model = MovieSession

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_session = self.get_object()

        cinema_hall = movie_session.cinema_hall
        rows_range = range(1, cinema_hall.rows + 1)
        seats_range = range(1, cinema_hall.seats_in_row + 1)

        tickets = movie_session.tickets.all()
        if len(tickets) == 0:
            tickets = [0]

        occupied_seats = Ticket.objects.filter(movie_session=movie_session).values_list('row', 'seat')

        context['movie_session'] = movie_session
        context['tickets'] = tickets
        context['rows_range'] = rows_range
        context['seats_range'] = seats_range
        context['occupied_seats'] = occupied_seats

        return context

