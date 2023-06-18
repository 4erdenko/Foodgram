from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/',
        include(
            [
                path('auth/', include('djoser.urls.authtoken')),
                path('users/', include('subscriptions.urls')),
                path('', include('users.urls')),
            ]
        ),
    ),
]
