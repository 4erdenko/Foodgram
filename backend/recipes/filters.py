from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    """FilterSet for filtering recipes."""

    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        """Filter recipes based on whether they are favorited by the user.

        Args:
            queryset (QuerySet): The initial queryset.
            name (str): The field name.
            value (bool): The filter value.

        Returns:
            QuerySet: The filtered queryset.

        """
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Filter recipes based on whether they are in the
        user's shopping cart.

        Args:
            queryset (QuerySet): The initial queryset.
            name (str): The field name.
            value (bool): The filter value.

        Returns:
            QuerySet: The filtered queryset.

        """
        if self.request.user.is_authenticated and value:
            return queryset.filter(shoppinglist__user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    """FilterSet for filtering ingredients."""

    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
