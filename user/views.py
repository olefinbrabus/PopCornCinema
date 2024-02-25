from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views import generic

from cinema.models import Ticket
from user.forms import UserForm
from user.models import User


class UserDetailView(LoginRequiredMixin,generic.DetailView):
    model = User
    template_name = 'user/account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        tickets = Ticket.objects.filter(order__user=user)
        context['tickets'] = tickets
        return context


class UserCreateView(generic.CreateView):
    form_class = UserForm
    success_url = "/user/login/"
    template_name = "user/register.html"


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', "birthday", "number", 'email','card']
    success_url = ".."
    template_name = "user/update.html"


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    fields = ['first_name', 'last_name', "birthday", "number", 'email','card']
    template_name = "user/delete_confim.html"