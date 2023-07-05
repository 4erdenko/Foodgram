from django.urls import path

from favorites.views import FavoriteViewSet

urlpatterns = [
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'favorite', 'delete': 'favorite'}),
    ),
]
