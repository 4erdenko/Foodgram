from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer

User = get_user_model()


class UserSubscriptionsListView(ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(follower=user)


class UserSubscribeView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response(
                {'detail': 'Подписка не найдена.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def create(self, request, id=None):
        try:
            following = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Пользователь не найден.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        follower = request.user
        if following == follower:
            return Response(
                {'detail': 'Нельзя подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription, created = Subscription.objects.get_or_create(
            follower=follower, following=following
        )
        if created:
            serializer = SubscriptionSerializer(
                subscription, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'detail': 'Вы уже подписаны на данного автора.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, id=None):
        following = User.objects.get(pk=id)
        follower = request.user
        try:
            subscription = Subscription.objects.get(
                follower=follower, following=following
            )
            subscription.delete()
            return Response(
                {'detail': 'Вы отписались от автора.'},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Subscription.DoesNotExist:
            return Response(
                {'detail': 'Вы не подписаны на данного автора.'},
                status=status.HTTP_404_NOT_FOUND,
            )
