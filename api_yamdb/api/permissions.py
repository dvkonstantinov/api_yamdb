from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                request.user == request.user.is_staff)
