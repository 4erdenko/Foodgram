import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Вы не можете использовать {value} '
            f'в качестве имени пользователя.'
        )

    invalid_chars = [
        char for char in value if not re.match(r'^[\w.@+-]+\Z', char)
    ]
    if invalid_chars:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы: '
            f'{", ".join(invalid_chars)}'
        )
