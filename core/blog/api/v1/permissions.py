from rest_framework import permissions

class IsOwnerOrReadonly(permissions.BasePermission):
    """
    Just owner of object has permission unless safe method 
    including 'GET', 'HEAD', 'OPTIONS'.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author.user == request.user