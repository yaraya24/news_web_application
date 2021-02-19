from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError




class IsAuthorizedUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        return obj == request.user