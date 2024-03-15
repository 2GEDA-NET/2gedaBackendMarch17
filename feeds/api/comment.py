
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db.models import F, Sum

from utils.exception import BadRequestException, NotFoundException
from utils.response import CustomResponse

from .. import models as m
from .. import serializers as s
from ..permissions import IsBlockedPost



class CommentPostAPIView(APIView):

    permission_classes = [IsAuthenticated, IsBlockedPost]

    parser_classes = (MultiPartParser,)

    def get(self, request: Request, post_id: int):

        comment_data = m.Comment.objects.filter(post=post_id).all()

        comments = [comment.to_dict() for comment in comment_data]

        context = {"comments": comments}

        return CustomResponse(data=context, message="get posts comments")

    def post(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        if not post:
            raise NotFoundException("this post does not exist")

        comment_serializer_context = {"post": post, "user": request.user}

        if request.data.get("file"):
            comment_serializer_context.update({"file": request.data.get("file")})

        serializer = s.CommentSerializer(
            data=request.data, context=comment_serializer_context
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        instance = serializer.save()

        context = {"comment": instance.to_dict()}

        return CustomResponse(
            data=context, message="created comment on post succussfuly"
        )


class SingleCommentAPIView(APIView):

    permission_classes = [IsAuthenticated, IsBlockedPost]

    parser_classes = (MultiPartParser,)

    def patch(self, request: Request, post_id: int, comment_id: int):

        comment_data = m.Comment.objects.filter(
            id=comment_id, post=post_id, user=request.user
        ).first()

        if not comment_data:
            raise NotFoundException("this comment does not exist")

        file_serializer = None

        if request.data.get("file"):

            file_serializer = s.CommentFileSerializer(
                data={"file": request.data.get("file")},
                context={
                    "file_type": request.data.get("file").content_type,
                    "comment": comment_data,
                },
            )

            if not file_serializer.is_valid():
                raise BadRequestException(
                    message=file_serializer.error_messages, data=file_serializer.errors
                )

        serializer = s.CommentSerializer(
            data=request.data, context={"comment": comment_data, "user": request.user}
        )

        if not serializer.is_valid():

            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        # Check whether there was an existing file, if user updates the comment with a file

        file_instance = None
        if file_serializer:
            if comment_data.file:
                comment_file_instance = comment_data.file

                file_path = comment_data.file.file.path

                default_storage.delete(file_path)

                comment_file_instance.delete()

                comment_data.file = None

            file_instance = file_serializer.save()

        comment_data.text_content = serializer.validated_data["text_content"]

        comment_data.file = file_instance

        comment_data.save()

        context = {"comment": comment_data.to_dict()}

        return CustomResponse(data=context, message="updated comment on post")

    def delete(self, request: Request, post_id: int, comment_id: int):

        comment_data = m.Comment.objects.filter(
            id=comment_id, post=post_id, user=request.user
        ).first()

        if not comment_data:
            raise NotFoundException("this comment does not exist")

        if comment_data.file:
            comment_file_instance = comment_data.file

            file_path = comment_data.file.file.path

            default_storage.delete(file_path)

            comment_file_instance.delete()

            comment_data.file = None

        comment_data.delete()

        return CustomResponse(message="deleted comment on post")


class ReactionCommentView(APIView):

    permission_classes = [IsAuthenticated, IsBlockedPost]

    def get(self, request: Request, post_id: int, comment_id: int):

        comment = m.Comment.objects.filter(id=comment_id, post=post_id).first()

        if not comment:
            raise NotFoundException("this comment does not exist")

        context = {
            "reactions": comment.get_reactions(),
            "comment": {"id": comment.id},
        }

        return CustomResponse(data=context, message="all reactions on this comment")

    def post(self, request: Request, post_id: int, comment_id: int):

        comment = m.Comment.objects.filter(id=comment_id, post=post_id).first()

        if not comment:
            raise NotFoundException("this comment does not exist")

        serializer = s.ReactionCommentSerializer(
            data=request.data, context={"comment": comment, "user": request.user}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        reaction = m.CommentReaction.objects.filter(
            comment=comment, user=request.user
        ).first()

        if reaction:

            if serializer.validated_data["reaction_type"] != reaction.reaction_type:

                if reaction.reaction_type == 1:

                    if comment.like_count > 0:
                        comment.like_count -= 1

                        if serializer.validated_data["reaction_type"] == 2:
                            comment.dislike_count += 1

                        elif serializer.validated_data["reaction_type"] == 3:
                            comment.love_count += 1

                        elif serializer.validated_data["reaction_type"] == 4:
                            comment.sad_count += 1

                        elif serializer.validated_data["reaction_type"] == 5:
                            comment.angry_count += 1

                elif reaction.reaction_type == 2:

                    if comment.dislike_count > 0:
                        comment.dislike_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        comment.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        comment.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        comment.sad_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        comment.angry_count += 1

                elif reaction.reaction_type == 3:

                    if comment.love_count > 0:
                        comment.love_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        comment.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        comment.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        comment.sad_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        comment.angry_count += 1

                elif reaction.reaction_type == 4:

                    if comment.sad_count > 0:

                        comment.sad_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        comment.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        comment.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        comment.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        comment.angry_count += 1

                elif reaction.reaction_type == 5:

                    if comment.angry_count > 0:
                        comment.angry_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        comment.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        comment.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        comment.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        comment.sad_count += 1

            comment.save()
            reaction.reaction_type = serializer.validated_data["reaction_type"]
            reaction.save()

        else:
            if serializer.validated_data["reaction_type"] == 1:
                comment.like_count += 1

            elif serializer.validated_data["reaction_type"] == 2:
                comment.dislike_count += 1

            elif serializer.validated_data["reaction_type"] == 3:
                comment.love_count += 1

            elif serializer.validated_data["reaction_type"] == 4:
                comment.sad_count += 1

            elif serializer.validated_data["reaction_type"] == 5:
                comment.angry_count += 1

            comment.save()
            instance = serializer.save()

        context = {
            "reaction": instance.to_dict() if not reaction else reaction.to_dict(),
            "comment": comment.to_dict(),
        }
        return CustomResponse(
            data=context, message="added reaction to comment succussfuly"
        )

    def delete(self, request: Request, post_id: int, comment_id: int):

        comment = m.Comment.objects.filter(id=comment_id, user=request.user).first()

        serializer = s.ReactionCommentSerializer(data=request.data)

        if not comment:
            raise NotFoundException("this comment does not exist")

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        reaction = m.CommentReaction.objects.filter(
            comment=comment,
            user=request.user,
            reaction_type=serializer.validated_data["reaction_type"],
        ).first()

        if reaction is None:

            raise BadRequestException("this reaction does not exist for this comment")

        if serializer.validated_data["reaction_type"] == 1:
            comment.like_count -= 1

        elif serializer.validated_data["reaction_type"] == 2:
            comment.dislike_count -= 1

        elif serializer.validated_data["reaction_type"] == 3:
            comment.love_count -= 1

        elif serializer.validated_data["reaction_type"] == 4:
            comment.sad_count -= 1

        elif serializer.validated_data["reaction_type"] == 5:
            comment.angry_count -= 1

        reaction.delete()

        comment.save()

        return CustomResponse(message="removed reaction succussfully")
    






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