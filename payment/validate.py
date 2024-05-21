from datetime import datetime

from cart.models import TicketTemp
from cinema.models import Ticket, MovieSession


def validate_tickets_in_cart(tickets: list[TicketTemp]) -> bool:
    for ticket in tickets:
        movie_session = MovieSession.objects.get(pk=ticket.movie_session_id)

        if not (
            is_session_not_time_over(movie_session) or
            is_ticket_not_exist(ticket, movie_session) or
            is_ticket_not_over_hall(ticket, movie_session)
        ):
            return False
    return True


def is_session_not_time_over(movie_session: MovieSession) -> bool:
    return movie_session.show_time.time() < datetime.now().time()


def is_ticket_not_over_hall(ticket: TicketTemp, session: MovieSession) -> bool:
    return Ticket.validate_ticket_without_error_message(
        row=ticket.row,
        seat=ticket.seat,
        cinema_hall=session.cinema_hall,
    )


def is_ticket_not_exist(ticket: TicketTemp, session: MovieSession) -> bool:
    return not Ticket.objects.filter(
        row=ticket.row,
        seat=ticket.seat,
        movie_session=session,
    ).first()
