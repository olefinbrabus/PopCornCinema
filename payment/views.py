
from django.views import generic


# Create your views here.


class PaymentSuccess(generic.TemplateView):
    template_name = "payment/payment_succes.html"
