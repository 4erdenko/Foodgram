from django.urls import path
from subscriptions.views import UserSubscribeView, UserSubscriptionsListView

urlpatterns = [
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
