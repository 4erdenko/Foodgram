from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from backend.wtf import DecryptView

urlpatterns = [
    path('wtf/', DecryptView.as_view(), name='wtf'),
    path('admin/', admin.site.urls),
    path(
        'api/',
        include(
            [
                path('auth/', include('djoser.urls.authtoken')),
                path('users/', include('subscriptions.urls')),
                path('', include('users.urls')),
                path('', include('favorites.urls')),
                path('', include('shoppinglist.urls')),
                path('', include('recipes.urls')),
            ]
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
