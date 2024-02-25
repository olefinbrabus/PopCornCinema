from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from cinema.views import MoviesDetailView, MoviesListView, MovieSessionDetailView

urlpatterns = [
    path("", MoviesListView.as_view(), name="movies-list"),
    path("<int:pk>", MoviesDetailView.as_view(), name="movies-detail"),
    path('sessions/<int:pk>/order/', MovieSessionDetailView.as_view(), name='movie_session_order'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "cinema"
