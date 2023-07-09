from django.urls import include, path
from rest_framework import routers

from favorites.views import FavoriteViewSet
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet

router = routers.DefaultRouter()

router.register('recipes', RecipeViewSet)
router.register('recipes', RecipeViewSet, basename='download_shopping_cart')
router.register('recipes', FavoriteViewSet, basename='favorite')
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)

urlpatterns = [path('', include(router.urls))]
