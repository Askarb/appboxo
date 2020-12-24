from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.method in SAFE_METHODS