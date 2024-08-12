from rest_framework.permissions import (
    BasePermission, SAFE_METHODS, IsAdminUser
)


class IsAdminOrSupUser(IsAdminUser):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False


class IsAdminOrModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.author == request.user
                    or request.user.is_moderator
                    or request.user.is_admin)
        return request.method in SAFE_METHODS


class IsAdminOrReadOnly(IsAdminOrSupUser):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or super().has_permission(request, view))
