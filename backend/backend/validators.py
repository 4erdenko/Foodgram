import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError("You can't use login me")

    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError('You can`t use this username')
