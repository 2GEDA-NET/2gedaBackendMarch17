from rest_framework import permissions

from feeds.models import Post
from utils.exception import BadRequestException, NotFoundException

from .models import BlockedUsers


class IsBlockedPost(permissions.BasePermission):
    def has_permission(self, request, view):
        post_id = view.kwargs.get("post_id")

        # Get the user that created the post
        post = Post.objects.filter(id=post_id).first()

        if post is None:
            raise NotFoundException("this post does not exist")

        # Get the user that created the post
        user = post.user.id

        # Check if the user making the request is blocked by the target user
        if BlockedUsers.objects.filter(user=user, blocked_user=request.user).exists():

            raise BadRequestException(
                message="You are blocked from accessing this user's content."
            )

        # Check if the user making the request has blocked the target user
        if BlockedUsers.objects.filter(user=request.user, blocked_user=user).exists():

            raise BadRequestException(
                message="You have blocked this user and cannot acccess thier post"
            )

        return True
