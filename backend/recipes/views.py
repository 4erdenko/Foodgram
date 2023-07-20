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
    """
    API endpoint that allows recipes to be viewed, created,
    updated, and deleted.

    Attributes:
        queryset (QuerySet): The queryset of Recipe objects.
        serializer_class (Serializer): The serializer class for Recipe objects.
        permission_classes (tuple): The permission classes applied to the view.
        filterset_class (FilterSet): The filterset class for Recipe filtering.
        filter_backends (tuple): The filter backends applied to the view.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrStuffOrReadOnly, IsAuthenticatedOrReadOnly)
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    @staticmethod
    def generate_pdf(user):
        """
        Generate a PDF file for the user's shopping cart.

        Args:
            user (User): The user object.

        Returns:
            BytesIO: The generated PDF file.
        """
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
        """
        Create an item using the specified serializer.

        Args:
            serializer_class (Serializer): The serializer class.
            data (dict): The data to be serialized.
            request (HttpRequest): The HTTP request.

        Returns:
            Response: The HTTP response.
        """
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_item(model, user, pk):
        """
        Delete an item with the specified model, user, and primary key.

        Args:
            model (Model): The model class.
            user (User): The user object.
            pk (int): The primary key of the item to be deleted.

        Returns:
            Response: The HTTP response.
        """
        get_object_or_404(model, user=user, recipe=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        """
        Add a recipe to the user's favorites.

        Args:
            request (HttpRequest): The HTTP request.
            pk (int): The primary key of the recipe.

        Returns:
            Response: The HTTP response.
        """
        data = {'user': request.user.id, 'recipe': pk}
        return self.create_item(FavoriteSerializer, data, request)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        """
        Remove a recipe from the user's favorites.

        Args:
            request (HttpRequest): The HTTP request.
            pk (int): The primary key of the recipe.

        Returns:
            Response: The HTTP response.
        """
        return self.delete_item(Favorite, self.request.user, pk)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        """
        Download the user's shopping cart as a PDF file.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            FileResponse: The HTTP response containing the PDF file.
        """
        time_format = '%d/%m - %H:%M'
        date = datetime.datetime.now().strftime(time_format)

        pdf = self.generate_pdf(request.user)

        return FileResponse(
            pdf, as_attachment=True, filename=f'Список покупок от {date}.pdf'
        )

    @action(detail=True, methods=['post'], url_path='shopping_cart')
    def add_to_cart(self, request, pk):
        """
        Add a recipe to the user's shopping cart.

        Args:
            request (HttpRequest): The HTTP request.
            pk (int): The primary key of the recipe.

        Returns:
            Response: The HTTP response.
        """
        data = {'user': request.user.id, 'recipe': pk}
        return self.create_item(ShoppingListSerializer, data, pk)

    @add_to_cart.mapping.delete
    def remove_from_cart(self, request, pk):
        """
        Remove a recipe from the user's shopping cart.

        Args:
            request (HttpRequest): The HTTP request.
            pk (int): The primary key of the recipe.

        Returns:
            Response: The HTTP response.
        """
        return self.delete_item(ShoppingList, request.user.id, pk)


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed, created,
    updated, and deleted.

    Attributes:
        queryset (QuerySet): The queryset of Ingredient objects.
        serializer_class (Serializer): The serializer class
        for Ingredient objects.
        filterset_class (FilterSet): The filterset class
        for Ingredient filtering.
        pagination_class (None): The pagination class for the view.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed, created, updated, and deleted.

    Attributes:
        queryset (QuerySet): The queryset of Tag objects.
        serializer_class (Serializer): The serializer class for Tag objects.
        pagination_class (None): The pagination class for the view.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
