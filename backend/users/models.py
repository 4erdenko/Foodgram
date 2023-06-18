from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True, validators=[EmailValidator(), MaxLengthValidator(254)]
    )
    username = models.CharField(
        verbose_name=_('username'),
        unique=True,
        max_length=150,
        validators=[
            MinLengthValidator(1),
            RegexValidator(regex=r'^[\w.@+-]+\Z'),
        ],
    )
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=150,
        validators=[MinLengthValidator(1), MaxLengthValidator(150)],
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=150,
        validators=[MinLengthValidator(1), MaxLengthValidator(150)],
    )
    password = models.CharField(
        verbose_name=_('password'),
        max_length=150,
        validators=[MinLengthValidator(8), MaxLengthValidator(150)],
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = 'id',

    def __str__(self):
        return self.username
