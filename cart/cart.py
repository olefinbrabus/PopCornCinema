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
        if self._validate_ticket_in_cart(ticket):
            self.cart[ticket_id] = {"movie_session_id": str(ticket.movie_session_id),
                                    "row": str(ticket.row), "seat": str(ticket.seat)}
            self.session.modified = True

    def _validate_ticket_in_cart(self, ticket: TicketTemp) -> bool:
        other_tickets = self.get_tickets()
        for other_ticket in other_tickets:
            if ticket == other_ticket:
                return False
        return True

    def get_tickets(self) -> list[TicketTemp]:
        lst = []
        for key, value in self.cart.items():
            movie_session_id = int(value["movie_session_id"])
            row = int(value["row"])
            seat = int(value["seat"])

            lst.append(TicketTemp(temp_id=key, movie_session_id=movie_session_id, row=row, seat=seat))
        return lst

    def __len__(self) -> int:
        return len(self.cart)
