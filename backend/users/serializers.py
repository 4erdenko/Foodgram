from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()


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
    is_subscribed = serializers.SerializerMethodField(read_only=True)

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


class UserSubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        from recipes.serializers import ShortRecipeSerializer

        limit = self.context['request'].query_params.get('limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]

        return ShortRecipeSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'follower',
            'following',
        )

    def validate(self, attrs):
        follower = attrs.get('follower')
        following = attrs.get('following')
        if follower == following:
            raise serializers.ValidationError(
                {'detail': 'Вы не можете подписаться на самого себя.'}
            )
        if Subscription.objects.filter(
            follower=follower, following=following
        ).exists():
            raise serializers.ValidationError(
                {'detail': 'Вы уже подписаны на этого пользователя.'}
            )
        return attrs
