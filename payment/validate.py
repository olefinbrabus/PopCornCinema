from cart.cart import Cart
from cart.models import TicketTemp
from cinema.models import Ticket, CinemaHall, MovieSession


def validate_tickets_in_cart(tickets: list[TicketTemp]) -> bool:
    for ticket in tickets:
        try:
            if Ticket.validate_ticket(
                    row=ticket.row,
                    seat=ticket.seat,
                    cinema_hall=MovieSession.objects.get(pk=ticket.movie_session_id).cinema_hall,
                    error_to_raise=ValueError
            ):
                Ticket.objects.get(
                    row=ticket.row,
                    seat=ticket.seat,
                    movie_session=MovieSession.objects.get(pk=ticket.movie_session_id),
                )
        except Ticket.DoesNotExist or ValueError as e:
            ...
        else:
            return False
    return True
