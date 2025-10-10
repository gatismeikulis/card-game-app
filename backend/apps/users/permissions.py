from typing import override
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from django.views.generic import View
from .models import User


class IsOwnerOrReadOnly(BasePermission):
    """Allow read for anyone, write only for owner"""

    @override
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
