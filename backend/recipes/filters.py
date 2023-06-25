from django_filters import rest_framework as filters
from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    name_starts = filters.CharFilter(
        field_name='name', lookup_expr='istartswith'
    )
    name_contains = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name_starts', 'name_contains')
