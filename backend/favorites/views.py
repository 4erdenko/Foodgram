from django.shortcuts import get_object_or_404
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from recipes.models import Recipe
from recipes.serializers import ShortRecipeSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet


class FavoriteViewSet(ViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def favorite(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                serializer = ShortRecipeSerializer(favorite.recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'detail': 'Рецепт уже добавлен в избранное.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:  # DELETE
            favorite = get_object_or_404(
                Favorite, user=request.user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
