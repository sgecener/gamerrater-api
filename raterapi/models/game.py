from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    designer = models.CharField(max_length=100)
    year = models.IntegerField()
    number_of_players = models.IntegerField()
    play_time = models.IntegerField()  # in minutes
    age = models.CharField(max_length=100)  # recommended age
    categories = models.ManyToManyField(
        "Category",
        through='GameCategory',
        related_name="games"
    )
    