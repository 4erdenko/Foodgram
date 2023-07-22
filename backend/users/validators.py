import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Validates the username field for a user.

    The username must not be in the list of forbidden usernames
    defined in the settings.
    It must also not contain any invalid characters.

    Args:
        value (str): The username value to validate.

    Raises:
        ValidationError: If the username is forbidden or contains
        invalid characters.
    """

    if value.lower() in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Вы не можете использовать {value} в качестве имени '
            f'пользователя.'
        )
    invalid_chars = set(re.findall(r'[^\w.@+-]', value))
    if invalid_chars:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы: '
            f'{", ".join(invalid_chars)}'
        )
