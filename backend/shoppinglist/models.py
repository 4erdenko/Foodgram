from django.conf import settings
from django.db import models
from recipes.models import Recipe


class ShoppingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)