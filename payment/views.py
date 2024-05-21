from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic

from cart.cart import Cart
from payment.create import create_order, create_tickets
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
        cart_tickets = cart.get_tickets
        if validate_tickets_in_cart(cart_tickets):
            order = create_order(request, cart)
            create_tickets(cart, order)
        else:
            raise TypeError("Сталася помилка при створенні заказу")

    except PermissionDenied as e:
        messages.success(request, f"{e}")
    except TypeError as e:
        messages.error(request, f"{e}")
    except ValidationError as e:
        messages.error(request, f"{e}")
    except Exception as e:
        messages.error(request, f"{e} Пришліть нам на пошту помилку, ми ії вирішимо!")

    else:
        messages.success(request, "Заказ успішно створений!")

    return redirect("index")


