from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Subscription

User = get_user_model()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(following=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='following.email', read_only=True)
    id = serializers.IntegerField(source='following.id', read_only=True)
    username = serializers.CharField(
        source='following.username', read_only=True
    )
    first_name = serializers.CharField(
        source='following.first_name', read_only=True
    )
    last_name = serializers.CharField(
        source='following.last_name', read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.follower.filter(following=obj.following).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.following)
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()

    def validate(self, data):
        user = self.context.get('request').user.id
        following = self.context.get('following')
        if user == following:
            raise serializers.ValidationError(
                {'detail': 'Вы не можете подписаться на себя'}
            )
        if Subscription.objects.filter(
            follower=user, following=following
        ).exists():
            raise serializers.ValidationError(
                {'detail': 'Вы уже подписаны на этого автора'}
            )
        return data

    def create(self, validated_data):
        follower_id = self.context.get('follower')
        following_id = self.context.get('following')
        instance = Subscription.objects.create(
            follower_id=follower_id,
            following_id=following_id,
        )
        return self.to_representation(instance)
