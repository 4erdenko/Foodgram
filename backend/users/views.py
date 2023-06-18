from djoser.views import UserViewSet

from .serializers import CustomUserCreateSerializer, CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    create_serializer_class = CustomUserCreateSerializer
