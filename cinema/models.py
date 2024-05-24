import os
import uuid
from datetime import datetime, date
from typing import Union

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(null=True, upload_to=movie_image_file_path)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ["-show_time"]

    @property
    def string_film_time(self) -> str:
        return time_to_string(self.show_time)


def time_to_string(time: Union[datetime, date], hours=True) -> str:
    str_time = ""

    if time.year != datetime.now().year:
        str_time += time.strftime("Рік: %y, ")

    day = time.strftime("%d ")
    str_time += day if day[0] != "0" else day[1:]

    months = ("січня", "лютого", "березня", "квітня", "травня", "червня",
              "липня", "серпня", "вересня", "жовтня", "листопада", "грудня")
    str_time += months[time.month - 1]

    if hours:
        str_time += time.strftime(" %H:%M")

    return str_time


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ["-created_at"]

    @property
    def string_created_time(self) -> str:
        return time_to_string(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    @staticmethod
    def validate_ticket_without_error_message(row, seat, cinema_hall):
        for ticket_attr_value, ticket_attr_name, cinema_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(cinema_hall, cinema_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                return False
        return True

    @staticmethod
    def validate_ticket(row, seat, cinema_hall, error_to_raise):
        for ticket_attr_value, ticket_attr_name, cinema_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(cinema_hall, cinema_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {cinema_hall_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.movie_session.cinema_hall,
            ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        unique_together = ("movie_session", "row", "seat")
        ordering = ["row", "seat"]
