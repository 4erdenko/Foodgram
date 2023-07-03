from django.urls import include, path
from rest_framework import routers

from favorites.views import FavoriteViewSet

urlpatterns = [
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'favorite', 'delete': 'favorite'}),
    ),
]
