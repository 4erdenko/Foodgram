from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """
    Configuration class for the 'recipes' app.

    Attributes:
        name (str): The name of the app.
        verbose_name (str): The human-readable name for the app.
    """

    name = 'recipes'
    verbose_name = 'Рецепты'
