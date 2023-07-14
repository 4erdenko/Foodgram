import datetime

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.cart_to_pdf import generate_pdf
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import Favorite, Ingredient, Recipe, ShoppingList, Tag
from recipes.permissions import IsAuthorOrStuffOrReadOnly
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 RecipeSerializer, ShoppingListSerializer,
                                 TagSerializer)


def create_item(serializer_class, data, context=None):
    serializer = serializer_class(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)


def delete_item(model, user, recipe):
    get_object_or_404(model, user=user, recipe=recipe).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrStuffOrReadOnly, IsAuthenticatedOrReadOnly)
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        time_format = '%d/%m - %H:%M'
        date = datetime.datetime.now().strftime(time_format)

        pdf = generate_pdf(request.user)

        return FileResponse(
            pdf, as_attachment=True, filename=f'Список покупок от {date}.pdf'
        )

    @action(detail=True, methods=['post'], url_path='shopping_cart')
    def add_to_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        return create_item(
            ShoppingListSerializer, data, context={'request': request}
        )

    @add_to_cart.mapping.delete
    def remove_from_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return delete_item(ShoppingList, request.user, recipe)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        return create_item(
            FavoriteSerializer, data, context={'request': request}
        )

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return delete_item(Favorite, request.user, recipe)
