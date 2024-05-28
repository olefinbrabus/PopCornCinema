from django.views import generic

from cinema.forms import *
from cinema.models import *


class IndexView(generic.ListView):
    template_name = "cinema/index.html"
    queryset = Movie.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Movie.objects.exists():
            main_movie = Movie.objects.get(pk=4)
            context['main_movie'] = main_movie

        return context


class CinemaListView(generic.ListView):
    template_name = "cinema/cinema_list_view.html"
    model = Cinema


class MoviesListView(generic.ListView):
    template_name = "cinema/movie_list.html"
    model = Movie
    paginate_by = 9

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

        if genre_id:
            conditions['genres'] = genre_id

        if is_active:
            conditions['is_active'] = is_active.lower() != 'true'

        self.request.session['search_params'] = {
            'genre': genre_id,
            'is_active': is_active,
        }

        if title:
            return queryset.filter(title__icontains=title, **conditions)
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

        hall_to_html = [
            (r_number + 1,
             [(s_number + 1, bool(Ticket.objects
                                  .filter(row=row, seat=seat, movie_session=movie_session).first()))
              for s_number, seat in enumerate(seats_range)])
            for r_number, row in enumerate(rows_range)
        ]

        context["hall_to_html"] = hall_to_html
        context['movie_session'] = movie_session

        return context
