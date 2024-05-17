from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views import generic

from cart.cart import Cart
from cart.models import TicketTemp
from cinema.models import Ticket, Order
from payment.validate import validate_tickets_in_cart


# Create your views here.


class PaymentCheck(generic.TemplateView):
    template_name = "payment/payment_check.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


def process_order(request):
    try:
        if not request.user.is_authenticated:
            raise PermissionDenied("Ви не увійшли в акаунт")

        cart = Cart(request)
        if validate_tickets_in_cart(cart.get_tickets):
            print("valid")

    except PermissionDenied as e:
        raise

    return redirect("index")
