from django.contrib.auth.models import AnonymousUser
from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import CustomUserSerializer, CustomUserCreateSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    create_serializer_class = CustomUserCreateSerializer
