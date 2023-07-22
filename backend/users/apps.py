from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the 'users' app.

    Attributes:
        name (str): The name of the app.
        verbose_name (str): The human-readable name for the app.
    """

    name = 'users'
    verbose_name = 'Пользователи'
