from rest_framework.permissions import BasePermission


class IsPollCreatorPermission(BasePermission):
    """Permission for Poll creator."""

    message = "Unauthorized. You must be the creator of this poll."

    def has_object_permission(self, request, view, obj):
        # Make user the obj creator has the right access.
        if obj.creator != request.user.profile:
            return False
        return True
