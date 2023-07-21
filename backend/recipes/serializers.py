from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.

    Fields:
        id (int): The ID of the tag.
        name (str): The name of the tag.
        color (str): The color of the tag.
        slug (str): The slug of the tag.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient model.

    Fields:
        id (int): The ID of the ingredient.
        name (str): The name of the ingredient.
        measurement_unit (str): The measurement unit of the ingredient.
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the RecipeIngredient model.

    Fields:
        id (int): The ID of the recipe ingredient.
        name (str): The name of the ingredient.
        measurement_unit (str): The measurement unit of the ingredient.
        amount (float): The amount of the ingredient.
    """
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):

    """
    Serializer for the Recipe model.

    Fields:
        id (int): The ID of the recipe.
        tags (list): The tags associated with the recipe.
        author (CustomUserSerializer): The author of the recipe.
        ingredients (list): The ingredients of the recipe.
        is_favorited (bool): Indicates if the recipe is favorited by the user.
        is_in_shopping_cart (bool): Indicates if the recipe is in the
        user's shopping cart.
        name (str): The name of the recipe.
        image (str): The URL of the recipe image.
        text (str): The text of the recipe.
        cooking_time (int): The cooking time of the recipe.
    """
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        """
        Get the 'is_favorited' field value.

        Args:
            obj (Recipe): The recipe object.

        Returns:
            bool: True if the recipe is favorited by the user, False otherwise.
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return obj.favorite.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        """
        Get the 'is_in_shopping_cart' field value.

        Args:
            obj (Recipe): The recipe object.

        Returns:
            bool: True if the recipe is in the user's shopping cart,
            False otherwise.
        """
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def validate(self, data):
        """
        Validate the ingredients field.

        Args:
            data (dict): The input data.

        Raises:
            serializers.ValidationError: If the ingredients are missing,
            duplicated, or have an invalid amount.

        Returns:
            dict: The validated data.
        """
        ingredients = self.initial_data.get('ingredients')
        ingredient_ids = [ingredient['id'] for ingredient in ingredients]
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Необходимо добавить ингредиенты.'}
            )
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                {'ingredients': 'Ингредиенты не должны повторяться.'}
            )

        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    {
                        'ingredients': 'Количество ингредиента '
                                       'должно быть больше 0.'}
                )

        return data

    def to_representation(self, instance):
        """
        Convert the instance to a representation.

        Args:
            instance (Recipe): The recipe instance.

        Returns:
            dict: The serialized representation of the recipe.
        """
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        representation['ingredients'] = RecipeIngredientSerializer(
            instance.recipes.all(), many=True
        ).data
        return representation

    def to_internal_value(self, data):
        """
        Convert the external data to internal value.

        Args:
            data (dict): The external data.

        Returns:
            dict: The internal value.
        """
        internal_value = super().to_internal_value(data)
        tags = data.get('tags')
        ingredients = data.get('ingredients')
        internal_value['tags'] = tags
        internal_value['ingredients'] = ingredients
        return internal_value

    def create_and_update_recipe_ingredients(self, recipe, ingredients):
        """
        Create and update the recipe ingredients.

        Args:
            recipe (Recipe): The recipe object.
            ingredients (list): The ingredients data.

        Returns:
            None
        """
        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=int(ingredient['amount']),
            )
            recipe_ingredients.append(recipe_ingredient)
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        """
        Create a new recipe.

        Args:
            validated_data (dict): The validated data.

        Returns:
            Recipe: The created recipe object.
        """
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        recipe.tags.set(tags)
        self.create_and_update_recipe_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Update an existing recipe.

        Args:
            instance (Recipe): The recipe object to update.
            validated_data (dict): The validated data.

        Returns:
            Recipe: The updated recipe object.
        """
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_and_update_recipe_ingredients(instance, ingredients)
        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model (short representation).

    Fields:
        id (int): The ID of the recipe.
        name (str): The name of the recipe.
        image (str): The URL of the recipe image.
        cooking_time (int): The cooking time of the recipe.
    """
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class BaseSerializer(ModelSerializer):
    """
    Base serializer for the Favorite and ShoppingList models.

    Fields:
        user (User): The user associated with the favorite/shopping list.
        recipe (Recipe): The recipe associated with the favorite/shopping list.
    """

    class Meta:
        fields = ('user', 'recipe')

    def validate(self, data):
        """
        Validate the serializer data.

        Args:
            data (dict): The serializer data.

        Raises:
            serializers.ValidationError: If the favorite/shopping
            list already exists.

        Returns:
            dict: The validated data.
        """
        user = data.get('user')
        recipe = data.get('recipe')
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {
                    'detail': f'Этот рецепт уже добавлен в '
                              f'{self.Meta.model._meta.verbose_name}.'
                }
            )
        return data


class FavoriteSerializer(BaseSerializer):
    """Serializer for the Favorite model."""

    class Meta(BaseSerializer.Meta):
        model = Favorite


class ShoppingListSerializer(BaseSerializer):
    """Serializer for the ShoppingList model."""

    class Meta(BaseSerializer.Meta):
        model = ShoppingList
