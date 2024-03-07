from rest_framework.permissions import BasePermission


class IsBusinessOwnerProfile(BasePermission):
    """Permission for user profile to be a business owner"""

    message = "This user profile is not business owner verified!"

    def has_permission(self, request, view):
        try:
            permission = request.user.is_verified and hasattr(
                request.user.profile, "business_owner"
            )
        except AttributeError:
            # user is anonymous user
            return False
        else:
            return permission
