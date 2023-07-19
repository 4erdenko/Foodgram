from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username

from backend import settings


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Пользователи',
        unique=True,
        max_length=settings.MAX_USERNAME_LENGTH,
        validators=(validate_username,),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_FIRST_NAME_LENGTH,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LAST_NAME_LENGTH,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.MAX_PASSWORD_NAME_LENGTH,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('follower', 'following'), name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F('following')),
                name='no_self_subscription',
            ),
        )

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'
