from cinema.models import MovieSession
from .models import TicketTemp


class Cart:
    def __init__(self, request):
        self.session = request.session

        key = "session_key"
        cart = self.session.get(key)

        if key not in request.session:
            cart = self.session[key] = {}

        self.cart = cart

    def add(self, ticket: TicketTemp) -> None:
        ticket_id = str(ticket.temp_id)
        if not self._is_contains_in_cart(ticket):
            self.cart[ticket_id] = {"movie_session_id": str(ticket.movie_session_id),
                                    "row": str(ticket.row), "seat": str(ticket.seat)}
            self.session.modified = True

    def _is_contains_in_cart(self, ticket: TicketTemp) -> bool:
        other_tickets = self.get_tickets

        for other_ticket in other_tickets:
            if ticket == other_ticket:
                return True
        return False

    @property
    def get_tickets(self) -> list[TicketTemp]:
        return [
            TicketTemp(temp_id=temp_id,
                       movie_session_id=int(value["movie_session_id"]),
                       row=int(value["row"]),
                       seat=int(value["seat"]))
            for temp_id, value in self.cart.items()
        ]

    def delete(self, ticket_id: str) -> None:
        if ticket_id in self.cart:
            del self.cart[ticket_id]

        self.session.modified = True

    def delete_all(self) -> None:
        self.cart.clear()

    @property
    def get_summary_tickets_price(self) -> float:
        cart_tickets = self.get_tickets

        sessions_id: set = {cart_ticket.movie_session_id for cart_ticket in cart_tickets}
        sessions = MovieSession.objects.filter(id__in=sessions_id)

        sum_price = float(sum([
            session.price for session in sessions
            for ticket in cart_tickets
            if session.id == ticket.movie_session_id
        ]))

        return int(sum_price) if sum_price.is_integer() else sum_price

    @property
    def get_sessions_in_tickets(self):
        sessions_id: set = {cart_ticket.movie_session_id for cart_ticket in self.get_tickets}
        return MovieSession.objects.filter(id__in=sessions_id)

    @property
    def get_tickets_price_by_sessions(self):
        tickets = self.get_tickets
        sessions = self.get_sessions_in_tickets
        price_sessions: list[str] = [""] * len(sessions)
        for i, session in enumerate(sessions):
            price = 0
            for ticket in tickets:
                if session.id == ticket.movie_session_id:
                    price += session.price

            price_sessions[i] = f"{session.movie.title}, {session.string_film_time}\n{price}"
        return price_sessions

    def __len__(self) -> int:
        return len(self.cart)
