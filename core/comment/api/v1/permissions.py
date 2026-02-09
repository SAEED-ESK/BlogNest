from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Just owner of object has permission.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
