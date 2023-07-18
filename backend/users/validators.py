import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Вы не можете использовать {value} в качестве имени пользователя.'
        )

    invalid_chars = set(re.findall(r'[^\w.@+-]', value))
    if invalid_chars:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы: '
            f'{", ".join(invalid_chars)}'
        )
