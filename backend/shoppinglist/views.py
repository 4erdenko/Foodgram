import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view, permission_classes, \
    authentication_classes
from rest_framework.response import Response

from shoppinglist.models import ShoppingList
from recipes.models import Recipe
from recipes.serializers import ShortRecipeSerializer
from shoppinglist.cart_to_pdf import generate_pdf
from shoppinglist.serializers import ShoppingListSerializer
from shoppinglist.models import ShoppingList
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class ShoppingListViewSet(ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = (IsAuthenticated,)

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def add_or_delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            add_to_card, created = ShoppingList.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                serializer = ShortRecipeSerializer(add_to_card.recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            elif ShoppingList.objects.filter(
                    user=request.user, recipe=recipe).exists():
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_shopping_card(request):
    time_format = '%d/%m - %H:%M'
    date = datetime.datetime.now().strftime(time_format)

    # Создайте PDF
    pdf = generate_pdf(request.user)

    # Верните PDF в ответе
    return FileResponse(pdf, as_attachment=True,
                        filename=f'Список покупок от {date}.pdf')

