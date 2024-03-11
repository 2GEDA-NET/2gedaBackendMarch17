from rest_framework.permissions import BasePermission


class IsBusinessAccount(BasePermission):
    """Permission for user profile to be a business owner"""

    message = "Unauthorized! Must have a business account!"

    def has_permission(self, request, view):
        try:
            permission = request.user.is_business
        except AttributeError:
            # user is anonymous user
            return False
        else:
            return permission
