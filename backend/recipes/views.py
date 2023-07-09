import datetime

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.permissions import IsAuthorOrStuffOrReadOnly
from recipes.serializers import (IngredientSerializer, RecipeSerializer,
                                 ShortRecipeSerializer, TagSerializer)
from shoppinglist.cart_to_pdf import generate_pdf
from shoppinglist.models import ShoppingList


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrStuffOrReadOnly, IsAuthenticatedOrReadOnly)
    filterset_class = RecipeFilter

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        time_format = '%d/%m - %H:%M'
        date = datetime.datetime.now().strftime(time_format)

        # Создайте PDF
        pdf = generate_pdf(request.user)

        # Верните PDF в ответе
        return FileResponse(
            pdf, as_attachment=True, filename=f'Список покупок от {date}.pdf'
        )

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def add_or_delete(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            add_to_card, created = ShoppingList.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                serializer = ShortRecipeSerializer(add_to_card.recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            elif ShoppingList.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(
                    {'detail': 'Рецепт уже в корзине'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif request.method == 'DELETE':
            shopping_card = get_object_or_404(
                ShoppingList, user=request.user, recipe=recipe
            )
            shopping_card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
