from django.urls import path

from payment.views import PaymentCheck, process_order

urlpatterns = [
    path('check', PaymentCheck.as_view(), name='payment-home'),
    path("process_order", process_order, name='payment-process'),
]
