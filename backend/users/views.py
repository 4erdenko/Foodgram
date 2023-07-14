from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.views import create_item

from .models import Subscription, User
from .serializers import SubscriptionSerializer


class UserSubscribeView(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['get'], url_path='subscriptions')
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(follower=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk):
        following = get_object_or_404(User, id=pk).id
        data = {'follower': self.request.user.id, 'following': following}
        print(f'validated_data_from_views: {data} in subscribe')
        return create_item(
            SubscriptionSerializer,
            data,
            context={
                'request': request,
                'follower': self.request.user.id,
                'following': following,
            },
        )

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
