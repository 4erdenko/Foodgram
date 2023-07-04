from favorites.models import Favorite
from recipes.serializers import ShortRecipeSerializer
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer


class FavoriteSerializer(ModelSerializer):
    recipe = ShortRecipeSerializer(read_only=True)
    user = ReadOnlyField(source='user.id')

    class Meta:
        model = Favorite
        fields = '__all__'
