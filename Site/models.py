from django.db import models
from django.contrib.auth.models import AbstractUser

class Game(models.Model):
    name = models.CharField(max_length=100)
    metacritic = models.TextField()
    description = models.TextField()
    IGN = models.TextField()
    general_rate = models.TextField()
    user_rate = models.TextField()
    game_informer = models.TextField()
    path_to_img = models.ImageField(upload_to='memes/')

    def get_absolute_url(self):
        return f'/game/id{self.id}'


class Account(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

class Raiting(models.Model):
    class Meta:
        unique_together = ('user', 'game')

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.IntegerField()
    suka = models.TextField()