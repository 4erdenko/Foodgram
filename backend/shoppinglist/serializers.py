from recipes.serializers import ShortRecipeSerializer
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from shoppinglist.models import ShoppingList


class ShoppingListSerializer(ModelSerializer):
    recipe = ShortRecipeSerializer(read_only=True)
    user = ReadOnlyField(source='user.id')

    class Meta:
        model = ShoppingList
        fields = '__all__'
