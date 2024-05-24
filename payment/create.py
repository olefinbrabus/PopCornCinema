from cinema.models import Ticket, MovieSession, Order


def create_order(request, cart) -> Order:
    order = Order(user=request.user, amount=cart.get_summary_tickets_price)
    order.save()
    return order


def create_tickets(cart, order: Order) -> None:
    tickets = cart.get_tickets

    for ticket in tickets:
        movie_session = MovieSession.objects.get(pk=ticket.movie_session_id)

        ticket = Ticket(
            row=ticket.row,
            seat=ticket.seat,
            order=order,
            movie_session=movie_session,
        )
        ticket.save()
