from django.db import models

from cinema.models import MovieSession


# temp model for cart
class TicketTemp(models.Model):
    temp_id = models.CharField(max_length=32, unique=True)
    movie_session_id = models.IntegerField()
    row = models.IntegerField()
    seat = models.IntegerField()

    def __hash__(self):
        return hash((self.temp_id, self.movie_session_id, self.row, self.seat))

    def __eq__(self, other):
        if isinstance(other, TicketTemp):
            print(self)
            print(other)
            return (self.movie_session_id == other.movie_session_id and
                    self.row == other.row and
                    self.seat == other.seat)
        return NotImplemented

    def __str__(self):
        return f'session: {self.movie_session_id} row: {self.row} seat: {self.seat}'
