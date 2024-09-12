from django.db import models
from django.contrib.auth.models import AbstractUser

class Game(models.Model):
    name = models.CharField(max_length=100)
    metacritic = models.FloatField()
    description = models.TextField()
    IGN = models.FloatField()
    general_rate = models.FloatField()
    user_rate = models.FloatField()
    game_informer = models.FloatField()
    path_to_img = models.ImageField(upload_to='games/')

    def get_absolute_url(self):
        return f'/game/id{self.id}'


class Account(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

class Rating(models.Model):
    class Meta:
        unique_together = ('user', 'game')

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.FloatField()