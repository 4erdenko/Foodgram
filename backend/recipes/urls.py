from django.urls import include, path
from rest_framework import routers

from recipes.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                           TagViewSet)

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('recipes', FavoriteViewSet, basename='favorite')
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)

urlpatterns = [path('', include(router.urls))]
