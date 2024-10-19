from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre_id  = models.IntegerField(unique=True,null=True,blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True,null=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_path = models.URLField()
    release_date = models.DateField()
    vote_average = models.FloatField()

    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'