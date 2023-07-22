from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username


class User(AbstractUser):
    """
    Custom user model representing a user of the application.

    Inherits from Django's AbstractUser model and adds additional fields.

    Attributes:
        email (EmailField): The email address of the user. Unique.
        username (CharField): The username of the user. Unique.
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        password (CharField): The password of the user.

    Meta:
        verbose_name (str): The human-readable name for the model.
        verbose_name_plural (str): The plural form of the model's name.
        ordering (tuple): The default ordering for the model's records.
    """

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Пользователь',
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
    """
    Model representing a subscription between users.

    Attributes:
        follower (ForeignKey): The user who is following another user.
        following (ForeignKey): The user being followed by another user.

    Meta:
        constraints (tuple): The model's constraints, including uniqueness
        and check constraints.
        verbose_name (str): The human-readable name for the model.
        verbose_name_plural (str): The plural form of the model's name.
    """

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
