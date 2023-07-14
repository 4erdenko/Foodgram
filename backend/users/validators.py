import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Вы не можете использовать {value} '
            f'в качестве имени пользователя.'
        )

    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            f'Вы не можете использовать это имя '
            f'пользователя.'
            f'Допустимы только буквы, цифры и следующие '
            f'символы: @, ., +, -'
        )
