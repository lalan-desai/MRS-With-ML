from django.contrib.auth.models import User
from django.db import models

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    languages = models.CharField(max_length=100)
    genres = models.CharField(max_length=100)
    

    def __str__(self):
        return self.user.username + "'s Preferences"



class Content(models.Model):
    imdbid = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    plot = models.TextField()
    language = models.CharField(max_length=100)
    poster =  models.URLField()
    imdbRating = models.FloatField()
    imdbVotes = models.BigIntegerField()
    type = models.CharField(max_length=10)


    def __str__(self):
        return self.title



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.username} {'liked' if self.has_liked else 'disliked'} {self.content.title}"
    
