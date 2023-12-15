from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is trying to access their own profile
        return request.method in SAFE_METHODS or obj.author == request.user