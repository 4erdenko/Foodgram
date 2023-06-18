from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'username', 'password', 'first_name', 'last_name')


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
