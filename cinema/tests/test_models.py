from datetime import datetime

from django.utils.timezone import make_aware
from django.test import TestCase
from cinema.models import MovieSession, Movie, CinemaHall, Actor


class ModelTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            duration=120,
            is_active=True
        )
        self.cinema_hall = CinemaHall.objects.create(
            name="Test Hall",
            rows=10,
            seats_in_row=10
        )
        self.movie_session = MovieSession.objects.create(
            show_time=make_aware(datetime.strptime("2024-09-05-11:45", "%Y-%m-%d-%H:%M")),
            movie=self.movie,
            cinema_hall=self.cinema_hall,
            price=100
        )
        self.actor = Actor.objects.create(
            first_name="Гаррі",
            last_name="Труман",
        )

    def test_movie_session_film_time(self):
        self.assertEqual(self.movie_session.string_film_time, "5 вересня 11:45")

    def test_cinema_hall_capacity(self):
        self.assertEqual(self.cinema_hall.capacity, 100)

    def test_actor_to_string(self):
        self.assertEqual(str(self.actor), "Гаррі Труман")


