from typing import override
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User
from .serializers import UserDetailSerializer, UserFullSerializer, UserListSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet[User]):
    queryset = User.objects.all()

    @override
    def get_serializer_class(self):
        """Different serializers for different actions [list, retrieve, create, update, partial_update, destroy]"""
        if self.action == "list":
            return UserListSerializer  # Public minimal data
        elif self.action == "retrieve":
            return UserDetailSerializer  # Public detailed data
        else:
            return UserFullSerializer  # Full data

    @override
    def get_permissions(self) -> list[BasePermission]:
        """Different permissions for different actions"""
        if self.action in ["list", "retrieve", "create"]:
            return [AllowAny()]
        elif self.action == "me":
            return [IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    # TODO: this override seems redundant, check with tests
    @override
    def get_object(self) -> User:
        """Ensure users can only modify their own user information"""
        obj = super().get_object()
        is_protected_action = self.action in ["update", "partial_update", "destroy"]
        is_owner = obj == self.request.user
        if is_protected_action and not is_owner:
            self.permission_denied(
                self.request, message="You can only modify your own user information"
            )
        return obj

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request: Request) -> Response:
        """GET /api/v1/users/me/ - Full info about authenticated user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
