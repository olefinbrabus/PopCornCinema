from django import forms
from user.models import User
from cinema.models import Order, Ticket


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'created_at',





