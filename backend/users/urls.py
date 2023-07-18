from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import SubscriptionsListView, UserSubscribeView

router = DefaultRouter()
router.register('users', UserSubscribeView, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionsListView.as_view(),
        name='subscriptions',
    ),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
