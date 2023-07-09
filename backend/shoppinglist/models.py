from django.conf import settings
from django.db import models

from recipes.models import Recipe, UserRelatedModel


class ShoppingList(UserRelatedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='рецепт',
    )

    class Meta(UserRelatedModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_shoppinglist'
            ),
        )

    def __str__(self):
        return (
            f'{self.recipe.name} в был добавлен в корзину пользователя'
            f' {self.user}'
        )
