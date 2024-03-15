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





class SingleReplyView(APIView):

    permission_classes = [IsAuthenticated, IsBlockedPost]

    def patch(self, request: Request, post_id: int, comment_id: int, reply_id: int):

        reply_data = m.Reply.objects.filter(
            id=reply_id, comment=comment_id, user=request.user
        ).first()

        if not reply_data:
            raise NotFoundException("this reply does not exist")

        serializer = s.ReplyCommentSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        reply_data.text_content = serializer.validated_data["text_content"]

        reply_data.save()

        context = {"reply": reply_data.to_dict()}

        return CustomResponse(data=context, message="updated reply on comment")

    def delete(self, request: Request, post_id: int, comment_id: int, reply_id: int):

        reply_data = m.Reply.objects.filter(
            id=reply_id, comment=comment_id, user=request.user
        ).first()

        if not reply_data:
            raise NotFoundException("this reply does not exist on this comment")

        reply_data.delete()

        return CustomResponse(message="deleted reply on comment")


class SingleReplyReactionView(APIView):

    permission_classes = [IsAuthenticated, IsBlockedPost]

    def get(self, request: Request, post_id: int, comment_id: int, reply_id: int):

        reply = m.Reply.objects.filter(
            id=reply_id, comment=comment_id, user=request.user
        ).first()

        if not reply:
            raise NotFoundException("this comment does not exist")

        context = {
            "reactions": reply.get_reactions(),
            "reply": {"id": reply.id},
        }

        return CustomResponse(data=context, message="all reactions on this reply")

    def post(self, request: Request, post_id: int, comment_id: int, reply_id: int):

        reply = m.Reply.objects.filter(
            id=reply_id, comment=comment_id, user=request.user
        ).first()

        if not reply:
            raise NotFoundException("this reply does not exist")

        serializer = s.ReactionReplySerializer(
            data=request.data, context={"reply": reply, "user": request.user}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        reaction = m.ReplyReaction.objects.filter(
            reply=reply, user=request.user
        ).first()

        if reaction:

            if serializer.validated_data["reaction_type"] != reaction.reaction_type:

                if reaction.reaction_type == 1:

                    if reply.like_count > 0:
                        reply.like_count -= 1

                        if serializer.validated_data["reaction_type"] == 2:
                            reply.dislike_count += 1

                        elif serializer.validated_data["reaction_type"] == 3:
                            reply.love_count += 1

                        elif serializer.validated_data["reaction_type"] == 4:
                            reply.sad_count += 1

                        elif serializer.validated_data["reaction_type"] == 5:
                            reply.angry_count += 1

                elif reaction.reaction_type == 2:

                    if reply.dislike_count > 0:
                        reply.dislike_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        reply.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        reply.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        reply.sad_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        reply.angry_count += 1

                elif reaction.reaction_type == 3:

                    if reply.love_count > 0:
                        reply.love_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        reply.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        reply.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        reply.sad_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        reply.angry_count += 1

                elif reaction.reaction_type == 4:

                    if reply.sad_count > 0:

                        reply.sad_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        reply.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        reply.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        reply.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        reply.angry_count += 1

                elif reaction.reaction_type == 5:

                    if reply.angry_count > 0:
                        reply.angry_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        reply.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        reply.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        reply.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        reply.sad_count += 1

            reply.save()
            reaction.reaction_type = serializer.validated_data["reaction_type"]
            reaction.save()

        else:
            if serializer.validated_data["reaction_type"] == 1:
                reply.like_count += 1

            elif serializer.validated_data["reaction_type"] == 2:
                reply.dislike_count += 1

            elif serializer.validated_data["reaction_type"] == 3:
                reply.love_count += 1

            elif serializer.validated_data["reaction_type"] == 4:
                reply.sad_count += 1

            elif serializer.validated_data["reaction_type"] == 5:
                reply.angry_count += 1

            reply.save()
            instance = serializer.save()

        context = {
            "reaction": instance.to_dict() if not reaction else reaction.to_dict(),
            "reply": reply.to_dict(),
        }
        return CustomResponse(
            data=context, message="added reaction to reply succussfuly"
        )

    def delete(self, request: Request, post_id: int, comment_id: int, reply_id: int):

        reply = m.Reply.objects.filter(
            id=reply_id, comment=comment_id, user=request.user
        ).first()

        serializer = s.ReactionReplySerializer(data=request.data)

        if not reply:
            raise NotFoundException("this reply does not exist")

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        reaction = m.ReplyReaction.objects.filter(
            reply=reply,
            user=request.user,
            reaction_type=serializer.validated_data["reaction_type"],
        ).first()

        if reaction is None:

            raise BadRequestException("this reaction does not exist for this reply")

        if serializer.validated_data["reaction_type"] == 1:
            reply.like_count -= 1

        elif serializer.validated_data["reaction_type"] == 2:
            reply.dislike_count -= 1

        elif serializer.validated_data["reaction_type"] == 3:
            reply.love_count -= 1

        elif serializer.validated_data["reaction_type"] == 4:
            reply.sad_count -= 1

        elif serializer.validated_data["reaction_type"] == 5:
            reply.angry_count -= 1

        reaction.delete()

        reply.save()

        return CustomResponse(message="removed reaction succussfully")