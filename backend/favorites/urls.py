from django.urls import include, path
from favorites.views import FavoriteViewSet
from rest_framework import routers

urlpatterns = [
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'favorite', 'delete': 'favorite'}),
    ),
]
