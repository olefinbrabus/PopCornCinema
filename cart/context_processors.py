from .cart import Cart
from .views import CartView


def cart(request):
    return {'cart': Cart(request)}
