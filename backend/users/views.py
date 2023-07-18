from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import SubscriptionSerializer, UserSubscriptionSerializer


class SubscriptionsListView(generics.ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return [
            subscription.following
            for subscription in Subscription.objects.filter(
                follower=self.request.user
            )
        ]


class UserSubscribeView(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk):
        data = {'follower': self.request.user.id, 'following': pk}
        serializer = SubscriptionSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        subscription = Subscription.objects.create(**serializer.validated_data)
        user = subscription.following
        context = {
            'request': request,
            'is_subscribed': True,
        }
        user_data = UserSubscriptionSerializer(user, context=context).data
        return Response(user_data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, pk=None):
        following = get_object_or_404(User, id=pk)
        follower = request.user
        subscription = get_object_or_404(
            Subscription, follower=follower, following=following
        )
        subscription.delete()
        return Response(
            {'detail': 'Вы отписались от автора.'},
            status=status.HTTP_204_NO_CONTENT,
        )
