from djoser.views import UserViewSet

from .serializers import CustomUserSerializer, CustomUserCreateSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    create_serializer_class = CustomUserCreateSerializer
