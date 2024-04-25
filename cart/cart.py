from typing import NoReturn

from .models import TicketTemp


class Cart:
    def __init__(self, request):
        self.session = request.session

        key = "session_key"
        cart = self.session.get(key)

        if key not in request.session:
            cart = self.session[key] = {}

        self.cart = cart

    def add(self, ticket: TicketTemp) -> NoReturn:
        ticket_id = str(ticket.temp_id)
        if self._validate_ticket(ticket):
            self.cart[ticket_id] = {"temp_id": str(ticket.temp_id), "movie_session_id": str(ticket.movie_session_id),
                                    "row": str(ticket.row), "seat": str(ticket.seat)}
            self.session.modified = True
            print("yes")
        else:
            print("no")

    def _validate_ticket(self, ticket: TicketTemp) -> bool:
        for key, value in self.cart.items():
            movie_session_id = int(value["movie_session_id"])
            row = int(value["row"])
            seat = int(value["seat"])

            other_ticket = TicketTemp(movie_session_id=movie_session_id, row=row, seat=seat)

            if other_ticket == ticket:
                return False
        return True
