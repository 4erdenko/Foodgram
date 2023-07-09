from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (UserSubscribeView, UserSubscriptionsListView,
                         UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'users/',
        include(
            [
                path(
                    'subscriptions/',
                    UserSubscriptionsListView.as_view(),
                    name='user-subscriptions',
                ),
                path(
                    '<int:id>/subscribe/',
                    UserSubscribeView.as_view(
                        {'post': 'subscribe', 'delete': 'unsubscribe'}
                    ),
                    name='user-subscribe',
                ),
            ]
        ),
    ),
    path('', include(router.urls)),
]
