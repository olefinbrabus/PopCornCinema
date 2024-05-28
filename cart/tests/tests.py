from datetime import datetime

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.timezone import make_aware

from cart.cart import Cart
from cinema.models import Movie, CinemaHall, MovieSession

SOME_PAGE = reverse('about')


class CartTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            duration=120,
            is_active=True
        )
        self.cinema_hall = CinemaHall.objects.create(
            id=1,
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

        self.factory: RequestFactory = RequestFactory()

    def _setup_session(self):
        self.request.COOKIES = {}
        middleware = SessionMiddleware(SOME_PAGE)
        middleware.process_request(self.request)
        self.request.session.save()

    def test_get_tickets(self):
        self.request = self.factory.post(
            '/cart/add/',
            {"session_id": "1", "row": "2", "seat": "4", "action": "post", "csrfmiddlewaretoken": "123dssd"},
            format='json'
        )
        self._setup_session()
        cart = Cart(self.request)

        self.assertTrue(isinstance(cart.get_tickets, list))
