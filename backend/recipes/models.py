from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Ingredient(models.Model):
    """
    Model representing an ingredient.

    Attributes:
        name (str): The name of the ingredient.
        measurement_unit (str): The unit of measurement for the ingredient.
    """

    name = models.CharField(
        max_length=settings.MAX_INGREDIENT_NAME_LENGTH,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=settings.MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    """
    Model representing a tag.

    Attributes:
        name (str): The name of the tag.
        color (str): The color of the tag.
        slug (str): The slug address of the tag.
    """

    name = models.CharField(
        max_length=settings.MAX_TAG_NAME_LENGTH,
        unique=True,
        verbose_name='Название',
    )
    color = models.CharField(
        max_length=settings.MAX_TAG_COLOR_LENGTH, verbose_name='Цвет'
    )
    slug = models.SlugField(unique=True, verbose_name='slug-адрес')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Model representing a recipe.

    Attributes:
        author (User): The author of the recipe.
        name (str): The name of the recipe.
        image (ImageField): The image of the recipe.
        text (str): The description of the recipe.
        ingredients (ManyToManyField): The ingredients used in the recipe.
        tags (ManyToManyField): The tags associated with the recipe.
        cooking_time (int): The cooking time of the recipe in minutes.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=settings.MAX_RECIPE_NAME_LENGTH,
        verbose_name='Название',
        unique=True,
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Тэги', related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                settings.MIN_COOKING_TIME,
                message='Время приготовления не может быть меньше 1 минуты',
            ),
            MaxValueValidator(
                settings.MAX_COOKING_TIME,
                message='Время приготовления не может быть больше 14 дней',
            ),
        ],
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} - {self.author}'


class RecipeIngredient(models.Model):
    """
    Model representing an ingredient used in a recipe.

    Attributes:
        recipe (Recipe): The recipe the ingredient is used in.
        ingredient (Ingredient): The ingredient.
        amount (int): The amount of the ingredient used in the recipe.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredient',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                settings.MIN_AMOUNT,
                message='Количество не может быть меньше 1',
            ),
            MaxValueValidator(
                settings.MAX_AMOUNT,
                message='Количество не может быть больше 1000',
            ),
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return (
            f'{self.recipe.name} - {self.ingredient.name} '
            f'({self.ingredient.measurement_unit})'
        )


class UserRelatedModel(models.Model):
    """
    Abstract base model representing a user-related model.

    Attributes:
        user (User): The user associated with the model instance.
        recipe (Recipe): The related recipe instance.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_%(class)s'
            )
        ]
        default_related_name = '%(class)s'

    def __str__(self):
        return f'{self.user} добавил в {self._meta.verbose_name} {self.recipe}'


class Favorite(UserRelatedModel):
    """
    Model representing a user's favorite recipe.

    Inherits from UserRelatedModel.
    """

    class Meta(UserRelatedModel.Meta):
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'


class ShoppingList(UserRelatedModel):
    """
    Model representing a user's shopping list.

    Inherits from UserRelatedModel.
    """

    class Meta(UserRelatedModel.Meta):
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
