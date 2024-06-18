from django.contrib.auth.models import User
from django.db import models

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    languages = models.CharField(max_length=100)
    genres = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username + "'s Preferences"


class Content(models.Model):
    imdbid = models.CharField(primary_key=True, max_length=12)
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    plot = models.TextField()
    language = models.CharField(max_length=100)
    poster =  models.CharField(max_length=250)
    imdbVotes = models.BigIntegerField()
    imdbRating = models.FloatField()

    def __str__(self):
        return self.title
