import uuid

from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import JsonResponse

from .cart import Cart
from cinema.models import MovieSession, Ticket
from .models import TicketTemp


# Create your views here.


class CartView(generic.TemplateView):
    template_name = "cart/cart_view.html"


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == "post":

        session_id = int(request.POST.get('session_id'))
        row = int(request.POST.get('row'))
        seat = int(request.POST.get('seat'))

        session = get_object_or_404(MovieSession, id=session_id)

        temp_id = uuid.uuid4()
        ticket = TicketTemp(temp_id=temp_id, movie_session_id=session.id, row=row, seat=seat)

        cart.add(ticket)

        response = JsonResponse({"Ticket Film": ticket.movie_session_id})
        return response


def cart_delete(request):
    pass


def cart_update(request):
    pass

