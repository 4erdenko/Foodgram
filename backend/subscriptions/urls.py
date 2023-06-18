from django.urls import path
from subscriptions.views import UserSubscriptionsListView, UserSubscribeView

urlpatterns = [
    path(
        'subscriptions/',
        UserSubscriptionsListView.as_view(),
        name='user-subscriptions',
    ),
    path(
        '<int:id>/subscribe/',
        UserSubscribeView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='user-subscribe',
    ),
]
