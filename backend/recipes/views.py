import datetime
import os
from io import BytesIO

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from recipes.permissions import IsAuthorOrStaffOrReadOnly
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 RecipeSerializer, ShoppingListSerializer,
                                 TagSerializer)
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from backend.mixins import CreateDeleteMixin


class RecipeViewSet(CreateDeleteMixin, ModelViewSet):
    """
    API endpoint that allows recipes to be viewed, created,
    updated, and deleted.

    This class also provides additional actions related to user's favorites
    and
    shopping cart.

    Inherits:
        CreateDeleteMixin: provides "create_item" and "delete_item" methods
        for
        handling 'favorite' and 'add_to_cart' actions.
        ModelViewSet: Django Rest Framework's ModelViewSet for basic CRUD
        operations.

    Attributes:
        queryset (QuerySet): The queryset of Recipe objects.
        serializer_class (Serializer): The serializer class for Recipe
        objects.
        permission_classes (tuple): The permission classes applied to the
        view.
        filterset_class (FilterSet): The filterset class for Recipe
        filtering.
        filter_backends (tuple): The filter backends applied to the view.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly, IsAuthenticatedOrReadOnly)
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
            settings.BASE_DIR, 'resources', 'fonts', 'Roboto-Medium.ttf'
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

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        """
        Add a recipe to the user's favorites.

        This action uses "create_item" method from
        CreateDeleteMixin to create
        new Favorite instance.

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

        This action uses "delete_item" method from CreateDeleteMixin to delete
        the Favorite instance.

        Args:
            request (HttpRequest): The HTTP request.
            pk (int): The primary key of the recipe.

        Returns:
            Response: The HTTP response.
        """
        return self.delete_item(Favorite, user=request.user, recipe=pk)

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

        This action uses "create_item" method from CreateDeleteMixin to create
        new ShoppingList instance.

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

        This action uses "delete_item" method from CreateDeleteMixin to delete
        the ShoppingList instance.

        Args:
            request (HttpRequest): The HTTP request.
            pk (int): The primary key of the recipe.

        Returns:
            Response: The HTTP response.
        """
        return self.delete_item(ShoppingList, user=request.user, recipe=pk)


class IngredientViewSet(ModelViewSet):
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


class TagViewSet(ModelViewSet):
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
