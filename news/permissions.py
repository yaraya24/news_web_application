from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError


class IsAuthorizedUser(permissions.BasePermission):
    """Permission that will restrict access if the logged in user
    isn't the same as the user object being requested"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user