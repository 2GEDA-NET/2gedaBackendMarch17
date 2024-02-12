from rest_framework.permissions import BasePermission


class HasStereoAccountPermission(BasePermission):
    """Permission class for user with a stereo account."""

    message = "Unauthorize. User must have a Stereo account."

    def has_permission(self, request, view):
        try:
            permission = hasattr(request.user.profile, "stereo_account")
        except AttributeError:
            # user is anonymous user
            return False
        else:
            if permission:
                return True
            return False
