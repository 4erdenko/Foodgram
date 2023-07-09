from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Subscription
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          SubscriptionSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    create_serializer_class = CustomUserCreateSerializer


def get_user(id):
    queryset = User.objects.all()
    return get_object_or_404(queryset, id=id)


class UserSubscriptionsListView(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(follower=user)


class UserSubscribeView(GenericViewSet):
    serializer_class = SubscriptionSerializer

    @action(detail=True, methods=['post'])
    def subscribe(self, request, id=None):
        following = get_user(id)
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
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'detail': 'Вы уже подписаны на данного автора.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=['delete'])
    def unsubscribe(self, request, id=None):
        following = get_user(id)
        follower = request.user
        if following == follower:
            return Response(
                {'detail': 'Вы настолько себя не любите?!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
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
