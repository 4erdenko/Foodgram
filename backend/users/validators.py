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
            f'\nВы не можете использовать {value} в качестве имени '
            f'пользователя.'
        )


def validate_password(value):
    """
    Validates the password for a user.

    The password must meet the following criteria:
    - Have at least 8 characters
    - Include at least one uppercase letter
    - Include at least one lowercase letter
    - Include at least one numeric digit
    - Include at least one special character
    - Must not include the characters "<" or ">"

    Args:
        value (str): The password value to validate.

    Raises:
        ValidationError: If the password does not meet the criteria.
    """

    if len(value) < 8:
        raise ValidationError(
            '\nПароль должен содержать как минимум 8 символов.')

    if not re.search(r'[A-Z]', value):
        raise ValidationError(
            '\nПароль должен содержать как минимум одну заглавную букву.')

    if not re.search(r'[a-z]', value):
        raise ValidationError(
            '\nПароль должен содержать как минимум одну строчную букву.')

    if not re.search(r'\d', value):
        raise ValidationError(
            '\nПароль должен содержать как минимум одну цифру.')

    if not re.search(r'[!@#$%^&*(),.?":{}|]', value):
        raise ValidationError(
            '\nПароль должен содержать как минимум один специальный символ.')

    invalid_chars = set(re.findall(r'[<>]', value))
    if invalid_chars:
        raise ValidationError(
            f'\nПароль содержит недопустимые символы: '
            f'{", ".join(invalid_chars)}'
        )
