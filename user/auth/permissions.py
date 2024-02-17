from rest_framework.permissions import BasePermission


class IsVerifiedPermission(BasePermission):
    """User must be verified."""

    message = "Unauthorized. Account must be verified."

    def has_permission(self, request, view):
        try:
            permission = request.user.is_verified
        except AttributeError:
            # user is anonymous user
            return False
        else:
            return permission
