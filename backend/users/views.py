from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import SubscriptionSerializer, UserSubscriptionSerializer


class UserSubscribeView(UserViewSet):
    """
    Custom view for user subscriptions.

    Extends the UserViewSet from djoser to provide additional
    subscription-related actions.
    """

    @action(detail=False)
    def subscriptions(self, request):
        """
        Get the subscriptions of the authenticated user.

        Returns the list of users that the authenticated user is subscribed to.

        Returns:
            Response: Paginated response containing the serialized
            user subscriptions.
        """
        queryset = Subscription.objects.filter(follower=request.user)
        page = self.paginate_queryset(queryset)
        serializer = UserSubscriptionSerializer(
            [subscription.following for subscription in page],
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, id):
        """
        Subscribe to a user.

        Creates a new subscription between the authenticated user
        and the specified user.

        Args:
            request (Request): The HTTP request object.
            id (int): The ID of the user to subscribe to.

        Returns:
            Response: The serialized data of the subscribed user.
        """
        data = {'follower': self.request.user.id, 'following': id}
        serializer = SubscriptionSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        user = subscription.following
        context = {
            'request': request,
            'is_subscribed': True,
        }
        user_data = UserSubscriptionSerializer(user, context=context).data
        return Response(user_data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        """
        Unsubscribe from a user.

        Deletes the subscription between the authenticated user
        and the specified user.

        Args:
            request (Request): The HTTP request object.
            id (int): The ID of the user to unsubscribe from.

        Returns:
            Response: Success message indicating that the user has
            been unsubscribed.
        """
        following = get_object_or_404(User, id=id)
        follower = self.request.user
        subscription = get_object_or_404(
            Subscription, follower=follower, following=following
        )
        subscription.delete()
        return Response(
            {'detail': 'Вы отписались от автора.'},
            status=status.HTTP_204_NO_CONTENT,
        )
