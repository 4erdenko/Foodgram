import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from shoppinglist.models import ShoppingList
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            image_format, image_string = data.split(';base64,')
            ext = image_format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(image_string), name=f'{uuid.uuid4()}.{ext}'
            )
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    # ingredients = RecipeIngredientSerializer(many=True)
    # tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        representation['ingredients'] = RecipeIngredientSerializer(
            instance.recipes.all(), many=True
        ).data
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        tags_data = data.get('tags')
        if not tags_data:
            raise serializers.ValidationError({'tags': 'Тэги не выбраны'})

        ingredients_data = data.get('ingredients')
        if not ingredients_data:
            raise serializers.ValidationError(
                {'ingredients': 'Ингредиенты не выбраны'}
            )

        for ingredient in ingredients_data:
            if not ingredient.get('id'):
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиент должен иметь id'}
                )
            if ingredient.get('amount', 0) <= 0:
                raise serializers.ValidationError(
                    {
                        'ingredients': 'Количество ингредиента '
                        'должно быть больше 0'
                    }
                )

        internal_value['tags'] = tags_data
        internal_value['ingredients'] = ingredients_data
        return internal_value

    def create(self, validated_data):
        name = validated_data.get('name')
        if Recipe.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                {'name': 'Рецепт с таким именем уже существует'}
            )
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        for tag_id in tags_data:
            recipe.tags.add(tag_id)
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data['id'],
                amount=ingredient_data['amount'],
            )
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])
        instance = super().update(instance, validated_data)
        instance.tags.set(tags_data)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient_id=ingredient_data['id'],
                amount=ingredient_data['amount'],
            )

        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
