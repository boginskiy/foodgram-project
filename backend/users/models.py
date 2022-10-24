from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределение базовой модели User."""

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_follower')
        ]
        ordering = ('id',)

    def __str__(self):
        return self.username


class UserFollowing(models.Model):
    """Пользователь user. Подписчики subscriber."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriber'],
                name='unique_subscriber'
            )
        ]
        ordering = ["-created"]
