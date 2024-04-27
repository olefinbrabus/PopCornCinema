import uuid
from datetime import datetime
from typing import Union, NoReturn

from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import JsonResponse, HttpResponse

from .cart import Cart
from cinema.models import MovieSession
from .models import TicketTemp


# Create your views here.


class CartView(generic.TemplateView):
    template_name = "cart/cart_view.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        cart = Cart(self.request)

        cart_tickets = cart.get_tickets()
        context["cart_tickets"] = cart_tickets

        sessions_id: set = {cart_ticket.movie_session_id for cart_ticket in cart_tickets}
        sessions = MovieSession.objects.filter(id__in=sessions_id)

        for session in sessions:
            session.show_time = string_film_time(session)
        context["sessions"] = sessions

        context["tickets_price"] = get_price(sessions, cart_tickets)

        return context


def string_film_time(session: MovieSession) -> str:
    str_time = ""
    session_time: datetime = session.show_time

    if session_time.year != datetime.now().year:
        str_time += session_time.strftime("Рік: %y, ")

    str_time += session_time.strftime(" %d ")

    months = ["січня", "лютого", "березня", "квітня", "травня", "червня",
              "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"]
    str_time += months[session_time.month - 1]

    str_time += session_time.strftime(" %H:%S")

    return str_time


def get_price(sessions: list[MovieSession], tickets: list[TicketTemp]) -> float:
    tickets_price: float = 0

    for session in sessions:
        for ticket in tickets:
            if session.id == ticket.movie_session_id:
                tickets_price += session.price

    return tickets_price


def cart_add(request) -> Union[HttpResponse, JsonResponse, NoReturn]:
    cart = Cart(request)

    if request.POST.get('action') == "post":
        session_id = int(request.POST.get('session_id'))
        row = int(request.POST.get('row'))
        seat = int(request.POST.get('seat'))

        session = get_object_or_404(MovieSession, id=session_id)

        temp_id = uuid.uuid4()
        ticket = TicketTemp(temp_id=temp_id, movie_session_id=session.id, row=row, seat=seat)

        cart.add(ticket)
        cart_quantity = len(cart)

        response = JsonResponse({"qty": cart_quantity})
        return response


def cart_delete(request):
    pass


def cart_update(request):
    pass
