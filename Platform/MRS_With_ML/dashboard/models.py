from django.contrib.auth.models import User
from django.db import models

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    languages = models.CharField(max_length=100)
    genres = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username + "'s Preferences"
