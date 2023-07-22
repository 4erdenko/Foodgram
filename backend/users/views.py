from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer, UserSubscriptionSerializer


class CreateDeleteMixin:
    """
    A mixin class that provides `create_item` and `delete_item` methods.
    These methods are used to create and delete instances of specified models.
    """

    def create_item(self, serializer_class, data, request):
        """
        Creates an instance of a specified model using the given serializer
        class and data.

        Args:
            serializer_class (Serializer): The serializer class to be used.
            data (dict): The data to be passed to the serializer.
            request (Request): The HTTP request object.

        Returns:
            Response: Response with a status of 201 (created).
        """
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete_item(self, model, **kwargs):
        """
        Deletes an instance of a specified model given its
        identifying attributes.

        Args:
            model (Model): The Django model class.
            **kwargs: The attributes identifying the model
            instance to be deleted.

        Returns:
            Response: Response with a status of 204 (no content).
        """
        get_object_or_404(model, **kwargs).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscribeView(CreateDeleteMixin, UserViewSet):
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
        return self.create_item(SubscriptionSerializer, data, request)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
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
        return self.delete_item(
            Subscription, follower=request.user, following__id=id
        )
