from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrStaffOrReadOnly(BasePermission):
    """
    Custom permission class that allows only the author of an object,
    staff users,
    or read-only access for other users.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request user has permission to perform the requested
        action on the object.
        """
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
        )
