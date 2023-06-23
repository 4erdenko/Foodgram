import base64
import uuid

from django.core.files.base import ContentFile
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}'
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
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipeingredient_set'
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe
