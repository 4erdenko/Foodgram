from django.contrib import admin
from django.contrib.admin import register

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)

admin.site.register(Favorite)
admin.site.register(ShoppingList)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time', 'favorites_count')
    search_fields = ('name', 'author')
    list_filter = ('author', 'name')
    inlines = [RecipeIngredientInline]

    @admin.display(description='счётчик избранного')
    def favorites_count(self, recipe):
        return recipe.favorites.count()


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')
