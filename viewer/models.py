from django.db import models
from django.db.models import Model, CharField, ForeignKey, IntegerField, TextField, DateField, DO_NOTHING, ManyToManyField, SET_NULL, DateTimeField

from django.contrib.auth.models import User

# Create your models here.

class Country(Model):
    name = CharField(max_length=64, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f'{self.name}'

class Genre(Model):
    name = CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'


class Person(Model):
    first_name = CharField(max_length=32, null=False, blank=False)
    last_name = CharField(max_length=32, null=False, blank=False)
    birth_date = DateField(null=True, blank=True)
    biography = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'birth_date']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Movie(Model):
    title_orig = CharField(max_length=64, null=False, blank=False)
    title_cz = CharField(max_length=64, null=True, blank=True)
    title_sk = CharField(max_length=64, null=True, blank=True)
    countries = ManyToManyField(Country, blank=True, related_name="movies_in_country")
    genres = ManyToManyField(Genre, blank=True, related_name="movies_of_genre")
    directors = ManyToManyField(Person, blank=True, related_name="directing_movie")
    actors = ManyToManyField(Person, blank=True, related_name="acting_in_movie")
    year = IntegerField(null=True, blank=True)
    # TODO ratings
    # TODO comments
    #  TODO images
    video = CharField(max_length=128, null=True, blank=True)
    description = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    # TODO: pokud existuje český/slovenksý název, tak ho zobrazit, jinak originální + do závorky zobrazit rok)
    # Příklad: Forrest Gump (1994)
    def __str__(self):
        if self.title_sk:
            return f"{self.title_sk}({self.year})"
        elif self.title_cz:
            return f"{self.title_cz}({self.year})"

        return f"{self.title_orig}({self.year})"
class Rating(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    rating = IntegerField(null=False, blank=False)

    def __str__(self):
        #return  f' {self.rating}% for {self.movie} by {self.user}'
        return f'{self.movie} - {self.rating}% by {self.user}'

class Comment(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    comment = TextField(null=False, blank=False)
    created = DateTimeField(auto_now_add=True)


    def __str__(self):
        # TODO: definovat __str__
        if len(self.comment) > 30:
            return f'{self.movie}: {self.user} - {self.comment[:50]}...'
        return f'{self.movie}: {self.user} - {self.comment}'

class Image(Model):
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, null=False, blank=False)
    url = CharField(max_length=128, null=False, blank=False)
    description = TextField()

    # TODO: definovat __str__
    def __str__(self):
        return f'{self.movie} - {self.description[:50]}'
