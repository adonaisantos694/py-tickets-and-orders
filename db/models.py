from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# -------------------
# User
# -------------------
class User(AbstractUser):
    pass


# -------------------
# Actor
# -------------------
class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


# -------------------
# Genre
# -------------------
class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


# -------------------
# Movie
# -------------------
class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return self.title


# -------------------
# Cinema Hall
# -------------------
class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return self.name


# -------------------
# Movie Session
# -------------------
class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {self.show_time}"


# -------------------
# Order
# -------------------
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


# -------------------
# Ticket
# -------------------
class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_per_seat"
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.movie_session} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall

        if self.row < 1 or self.row > hall.rows:
            raise ValidationError(
                {
                    "row": (
                        "row number must be in available range: "
                        f"(1, rows): (1, {hall.rows})"
                    )
                }
            )

        if self.seat < 1 or self.seat > hall.seats_in_row:
            raise ValidationError(
                {
                    "seat": (
                        "seat number must be in available range: "
                        f"(1, seats_in_row): "
                        f"(1, {hall.seats_in_row})"
                    )
                }
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
