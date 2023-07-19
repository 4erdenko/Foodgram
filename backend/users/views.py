from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import SubscriptionSerializer, UserSubscriptionSerializer


class UserSubscribeView(UserViewSet):
    @action(detail=False)
    def subscriptions(self, request):
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
