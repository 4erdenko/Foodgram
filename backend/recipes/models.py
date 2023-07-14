from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# -------------------------------------------------------------------------- #
# ---------------------------  Ingredient  --------------------------------- #
# -------------------------------------------------------------------------- #
class Ingredient(models.Model):
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


# -------------------------------------------------------------------------- #
# ----------------------------      Tag    --------------------------------- #
# -------------------------------------------------------------------------- #


class Tag(models.Model):
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


# -------------------------------------------------------------------------- #
# ---------------------------  Recipes part  ------------------------------- #
# -------------------------------------------------------------------------- #


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=settings.MAX_RECIPE_NAME_LENGTH, verbose_name='Название'
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


# -------------------------------------------------------------------------- #
# ------------------------  UserRelatedModel  ------------------------------ #
# -------------------------------------------------------------------------- #


class UserRelatedModel(models.Model):
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

    def __str__(self):
        return f'{self.user} добавил в {self._meta.verbose_name} {self.recipe}'


class Favorite(UserRelatedModel):
    class Meta(UserRelatedModel.Meta):
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'
        default_related_name = 'favorites'


# -------------------------------------------------------------------------- #
# ------------------------  ShoppingList  ---------------------------------- #
# -------------------------------------------------------------------------- #


class ShoppingList(UserRelatedModel):
    class Meta(UserRelatedModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_lists'
