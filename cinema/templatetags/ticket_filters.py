# cinema/templatetags/ticket_filters.py
from django import template
from cinema.models import Ticket

register = template.Library()

@register.filter
def seat_available(available_seats, row, seat, cinema_hall):
    # Реализация вашей логики для проверки доступности места
    # Например, можно проверить, есть ли соответствующий билет в available_seats
    return Ticket.objects.filter(
        row=row, seat=seat, movie_session__cinema_hall=cinema_hall
    ).exists()
