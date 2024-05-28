import io
from os import remove

import qrcode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from cinema.models import Ticket, Order
from user.forms import UserCreateForm, UserChangedForm, UserPasswordChangedForm
from user.models import User


class UserDetailView(LoginRequiredMixin, generic.DetailView):

    model = User
    template_name = 'user/account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        orders = Order.objects.filter(user=user)
        tickets = Ticket.objects.filter(order__user=user)
        context["orders"] = orders
        context["tickets"] = tickets

        return context


class UserCreateView(generic.CreateView):
    form_class = UserCreateForm
    success_url = "/user/login/"
    template_name = "user/register.html"


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserChangedForm
    success_url = "/"
    template_name = "user/update.html"


def user_update_password_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            pass
        else:
            form = UserPasswordChangedForm(user)
            return render(request, "user/update_password.html", {"form": form})
    else:
        messages.success(request, "Ви не зареєстровані")
        redirect("index")


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    fields = ['first_name', 'last_name', "birthday", "number", 'email', 'card']
    template_name = "user/delete_confim.html"


class OrderListUserView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user/order_list_user_view.html'
    paginate_by = 10

    ordering = ['-created_at']


@login_required
def order_pdf_download_view(request, pk):
    if request.method == 'GET':
        order = Order.objects.filter(id=pk).first()
        tickets = Ticket.objects.filter(order=order)

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        width, height = letter
        pdfmetrics.registerFont(TTFont('Monaco', 'static/pdf_font/Monaco.ttf'))

        for ticket in tickets:
            c.setFillColor(colors.red)
            c.rect(0, 0, width, height, fill=1)

            c.setFillColor(colors.white)
            margin = 0.5 * inch
            c.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=1)

            c.setFont("Monaco", 14)
            c.setFillColor(colors.black)

            generate_qrcode_image(ticket, order)

            c.drawString(margin + inch, height - margin - 2.2 * inch, f"Фильм: {ticket.movie_session.movie.title}")
            c.drawString(margin + inch, height - margin - 2.4 * inch, f"Час: {ticket.movie_session.string_film_time}")
            c.drawString(margin + inch, height - margin - 2.6 * inch, f"Місто: {ticket.row}, Ряд: {ticket.seat}")
            c.drawString(margin + inch, height - margin - 2.8 * inch, f"Ціна заказу: {order.amount}")
            c.drawString(margin + inch, height - margin - 2 * inch, f"Дата заказу: {order.string_created_time}")
            c.drawImage(ImageReader("qrcode.png"), 100, 100, height=200, width=200)

            remove("qrcode.png")

            c.line(100, 650, 500, 650)
            c.line(100, 300, 500, 300)
            c.setFillColorRGB(0.5, 0, 0)
            c.drawString(margin + inch, height - margin - 1 * inch, "PopCornCinema")

            c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"Білети-{order.id}-PopCornCinema.pdf")


def generate_qrcode_image(ticket: Ticket, order: Order, filename='qrcode.png'):
    ticket_values = (ticket.movie_session.movie.title, ticket.movie_session.string_film_time,
                     str(ticket.row), str(ticket.seat), str(order.amount), order.string_created_time)
    a = "".join(ticket_values).replace(" ", ";")
    img = qrcode.make(a)
    img.save(filename)

