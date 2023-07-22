from django.contrib import admin
from django.contrib.admin import register
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)

admin.site.register(Favorite)
admin.site.register(ShoppingList)


class RecipeIngredientInline(admin.TabularInline):
    """
    Inline model for RecipeIngredient in RecipeAdmin.

    Attributes:
        model (Model): The model class for RecipeIngredient.
        extra (int): The number of extra inline forms to display.
    """

    model = RecipeIngredient
    extra = 1


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin model for Recipe.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to search in the admin interface.
        list_filter (tuple): The fields to use for filtering in the
        admin interface.
        inlines (list): The inline models to include.
    """

    list_display = ('id', 'name', 'author', 'cooking_time', 'favorites_count')
    search_fields = ('name', 'author')
    list_filter = ('author', 'name')
    inlines = [RecipeIngredientInline]

    @admin.display(description='счётчик избранного')
    def favorites_count(self, recipe):
        """
        Display the count of favorites for a recipe.

        Args:
            recipe (Recipe): The Recipe object.

        Returns:
            int: The count of favorites.
        """
        return recipe.favorite.count()


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Admin model for Ingredient.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to search in the admin interface.
        list_filter (tuple): The fields to use for filtering in the
        admin interface.
    """

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin model for Tag.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to search in the admin interface.
        list_filter (tuple): The fields to use for filtering in the
        admin interface.
    """

    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """
    Admin model for RecipeIngredient.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to search in the admin interface.
        list_filter (tuple): The fields to use for filtering in the
        admin interface.
    """

    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')
