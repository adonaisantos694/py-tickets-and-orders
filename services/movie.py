from typing import Optional, QuerySet
from db.models import Movie
from django.db import transaction


def get_movies(title: Optional[str] = None) -> QuerySet[Movie]:
    queryset = Movie.objects.all()
    if title:
        queryset = queryset.filter(title__icontains=title)
    return queryset


@transaction.atomic
def create_movie(
    title: str,
    description: str,
    genres,
    actors,
) -> Movie:
    movie = Movie.objects.create(title=title, description=description)
    movie.genres.set(genres)
    movie.actors.set(actors)
    return movie
