from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from django.db.models import F, Sum

from utils.exception import BadRequestException, NotFoundException
from utils.response import CustomResponse

from .. import models as m
from .. import serializers as s
from .. import mime_types as mime
from ..permissions import IsBlockedPost

class StatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser,)

    def get(self, request: Request):

        status_data = [
            status.to_dict()
            for status in m.Status.objects.filter(user=request.user).all()
        ]

        context = {"status": status_data}

        return CustomResponse(
            data=context,
            message="all created status",
        )

    def post(self, request: Request):

        serializer = s.StatusSerializer(
            data=request.data, context={"user": request.user}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        instance = serializer.save()

        context = {"status": instance.to_dict()}

        return CustomResponse(
            data=context,
            message="created status successfully",
            status=status.HTTP_201_CREATED,
        )


class SingleStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, status_id: int):

        status_data = m.Status.objects.filter(id=status_id).first()

        if status_data is None:
            raise NotFoundException("this status does not exist for this user")

        context = {"status": status_data.to_dict()}

        return CustomResponse(data=context, message="get single status")

    def delete(self, request: Request, status_id: int):

        status_data = m.Status.objects.filter(id=status_id, user=request.user).first()

        if status_data is None:
            raise NotFoundException("this status does not exist for this user")

        status_data.delete()

        return CustomResponse(
            message="deleted status successfully",
        )


class ReplyCommentView(APIView):

    permission_classes = [IsAuthenticated, IsBlockedPost]

    def get(self, request: Request, post_id: int, comment_id: int):

        replies_with_engagements = m.Reply.objects.filter(comment=comment_id).annotate(
            total_engagements=Sum(
                F("like_count")
                + F("dislike_count")
                + F("sad_count")
                + F("angry_count")
                + F("love_count")
            ),
        )

        ordered_replies = replies_with_engagements.order_by("-total_engagements")

        replies = [reply.to_dict() for reply in ordered_replies]

        context = {"replies": replies}

        return CustomResponse(data=context, message="get replies for comments")

    def post(self, request: Request, post_id: int, comment_id: int):

        comment = m.Comment.objects.filter(id=comment_id, post=post_id).first()

        if not comment:
            raise NotFoundException("this comment does not exist")

        serializer = s.ReplyCommentSerializer(
            data=request.data, context={"user": request.user, "comment": comment}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        instance = serializer.save()

        context = {"reply": instance.to_dict()}

        return CustomResponse(
            data=context,
            message="added reply successfully",
        )