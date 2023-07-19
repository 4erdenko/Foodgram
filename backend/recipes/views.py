import datetime
import os
from io import BytesIO

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from recipes.permissions import IsAuthorOrStuffOrReadOnly
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 RecipeSerializer, ShoppingListSerializer,
                                 TagSerializer)
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrStuffOrReadOnly, IsAuthenticatedOrReadOnly)
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    @staticmethod
    def generate_pdf(user):
        font_path = os.path.join(
            settings.BASE_DIR, 'static', 'fonts', 'Roboto-Medium.ttf'
        )

        pdfmetrics.registerFont(TTFont('Roboto-Medium', font_path))

        ingredients = (
            RecipeIngredient.objects.filter(recipe__shoppinglist__user=user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
        )

        buffer = BytesIO()
        page = canvas.Canvas(buffer, pagesize=letter)

        text = page.beginText(70, 700)
        text.setFont('Roboto-Medium', 24)

        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            total = ingredient['total_amount']
            text.textLine(f'{name} ({unit}) — {total}')

        page.drawText(text)
        page.showPage()
        page.save()

        buffer.seek(0)
        return buffer

    @staticmethod
    def create_item(serializer_class, data, request):
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_item(model, user, pk):
        get_object_or_404(model, user=user, recipe=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        return self.create_item(FavoriteSerializer, data, request)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        return self.delete_item(Favorite, self.request.user, pk)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        time_format = '%d/%m - %H:%M'
        date = datetime.datetime.now().strftime(time_format)

        pdf = self.generate_pdf(request.user)

        return FileResponse(
            pdf, as_attachment=True, filename=f'Список покупок от {date}.pdf'
        )

    @action(detail=True, methods=['post'], url_path='shopping_cart')
    def add_to_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        return self.create_item(ShoppingListSerializer, data, pk)

    @add_to_cart.mapping.delete
    def remove_from_cart(self, request, pk):
        return self.delete_item(ShoppingList, request.user.id, pk)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
