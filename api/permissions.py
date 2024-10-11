from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)


class IsAuthorOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.created_by == request.user
        )
