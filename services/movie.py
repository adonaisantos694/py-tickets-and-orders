from django.db import transaction
from db.models import Movie


def get_movies(title=None):
    queryset = Movie.objects.all()
    if title:
        queryset = queryset.filter(title__icontains=title)
    return queryset


@transaction.atomic
def create_movie(title, description, genres, actors):
    movie = Movie.objects.create(title=title, description=description)
    movie.genres.set(genres)
    movie.actors.set(actors)
    return movie
