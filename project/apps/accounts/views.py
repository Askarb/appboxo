from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts.permissions import IsOwner
from apps.accounts.serializers import UserSerializer, UserLoginSerializer, UserCreateSerializer, UserUpdateSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsOwner,)
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer

    @action(methods=['post'], permission_classes=[AllowAny], detail=False)
    def login(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
