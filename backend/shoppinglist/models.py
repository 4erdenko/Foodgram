from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe


class ShoppingList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=_('shopping_cart'),
        verbose_name=_('user'),
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.recipe.name} в был добавлен в корзину пользователя'
                f' {self.user}')
