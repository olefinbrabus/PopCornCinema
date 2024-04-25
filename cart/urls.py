from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path('add/', cart_add, name="cart_add"),
    path('delete/', cart_delete, name="cart_delete"),
    path('update/', cart_update, name="cart_update"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'cart'
