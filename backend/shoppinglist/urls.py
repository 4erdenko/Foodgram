from django.urls import path
from shoppinglist.views import ShoppingListViewSet, download_shopping_card

urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingListViewSet.as_view(
        {'delete': 'add_or_delete', 'post': 'add_or_delete'})),
    path('recipes/download_shopping_cart/', download_shopping_card)

]