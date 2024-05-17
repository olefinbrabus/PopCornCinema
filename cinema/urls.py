from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from cinema.views import MoviesDetailView, MoviesListView, MovieSessionDetailView, CinemaHallListView

urlpatterns = [
    path("", MoviesListView.as_view(), name="movies-list"),
    path("<int:pk>", MoviesDetailView.as_view(), name="movies-detail"),
    path("sessions/<int:pk>/order/", MovieSessionDetailView.as_view(), name="movie_session_order"),
    path("cinemahalls", CinemaHallListView.as_view(), name="cinema_hall_list_view")
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "cinema"
