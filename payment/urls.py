from django.urls import path

from payment.views import PaymentSuccess

urlpatterns = [
    path('success', PaymentSuccess.as_view(), name='payment-home'),
]
