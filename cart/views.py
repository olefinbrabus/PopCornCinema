import uuid
from typing import Union

from django.contrib import messages
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

        cart_tickets = cart.get_tickets
        context["cart_tickets"] = cart_tickets

        sessions_id: set = {cart_ticket.movie_session_id for cart_ticket in cart_tickets}
        sessions = MovieSession.objects.filter(id__in=sessions_id)

        context["sessions"] = sessions

        context["tickets_summary_price"] = cart.get_summary_tickets_price
        context["tickets_price_sessions"] = cart.get_tickets_price_by_sessions

        return context


def cart_add(request) -> Union[HttpResponse, JsonResponse, None]:
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
    cart = Cart(request)
    if request.POST.get('action') == "post":
        ticket_id: str = request.POST.get('ticket_id')
        cart.delete(ticket_id=ticket_id)

        response = JsonResponse({"ticket": ticket_id})
        return response


def cart_update(request):
    pass
