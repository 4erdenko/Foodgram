from django.contrib.auth import get_user_model
from rest_framework import serializers
from subscriptions.models import Subscription
from users.serializers import CustomUserSerializer

User = get_user_model()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('following',)

    def to_representation(self, instance):
        serializer = CustomUserSerializer(
            instance.following, context=self.context
        )
        return serializer.data
