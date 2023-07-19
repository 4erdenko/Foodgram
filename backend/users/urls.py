from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserSubscribeView

router = DefaultRouter()

router.register('users', UserSubscribeView, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
