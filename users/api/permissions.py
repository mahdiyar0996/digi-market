from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class FullPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id == view.kwargs.get('pk'):
            return True
        if request.user.is_superuser or request.user.is_staff:
            return True

