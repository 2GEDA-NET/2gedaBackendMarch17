from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from utils.exception import BadRequestException, NotFoundException
from utils.response import CustomResponse

from . import models as m
from . import serializers as s
from django.core.files.storage import default_storage

from .permissions import IsBlockedPost


class PostAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        post_data = m.Post.objects.filter(user=request.user).all()

        posts = [post.to_dict() for post in post_data]

        context = {"posts": posts}

        return CustomResponse(data=context, message="get user's posts")

    def post(self, request: Request):

        serializer = s.PostSerializer(data=request.data, context={"user": request.user})

        if not serializer.is_valid():
            raise APIException(serializer.errors, status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()

        context = {"post": instance.to_dict()}

        return CustomResponse(data=context, message="created post succussfuly")


# This api class based view is responsible for handling request in the format post/<int:id>
# This is to make any changes (update or delete) to a single post
class SinglePostView(APIView):

    permission_classes = [IsAuthenticated]  # IsBlockedPost]

    def get(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        if post is None:
            raise NotFoundException("this post does not exist")

        context = {"post": post.to_dict()}

        return CustomResponse(data=context, message="get post successfully")

    def patch(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        if post is None:
            raise NotFoundException("this post does not exist")

        serializer = s.PostSerializer(instance=post, data=request.data, partial=True)

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        instance = serializer.save()

        context = {"post": instance.to_dict()}

        return CustomResponse(data=context, message="updated post successfully")

    def delete(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id, user=request.user).first()

        if post is None:
            raise NotFoundException("this post does not exist")

        post.delete()

        return CustomResponse(message="deleted post successfully")


class ReactionPostView(APIView):

    permission_classes = [IsAuthenticated]  # IsBlockedPost]

    def get(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        if not post:
            raise NotFoundException("this post does not exist")

        context = {
            "reactions": post.get_total_post_reactions(),
            "post": {"id": post.id},
        }

        return CustomResponse(data=context, message="all reactions on this post")

    def post(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        if not post:
            raise NotFoundException("this post does not exist")

        serializer = s.ReactionPostSerializer(
            data=request.data, context={"post": post, "user": request.user}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        reaction = m.PostReaction.objects.filter(post=post, user=request.user).first()

        if reaction:

            if serializer.validated_data["reaction_type"] != reaction.reaction_type:
                if reaction.reaction_type == 1:
                    if post.like_count > 0:
                        post.like_count -= 1

                        if serializer.validated_data["reaction_type"] == 2:
                            post.dislike_count += 1

                        elif serializer.validated_data["reaction_type"] == 3:
                            post.love_count += 1

                        elif serializer.validated_data["reaction_type"] == 4:
                            post.sad_count += 1

                        elif serializer.validated_data["reaction_type"] == 5:
                            post.angry_count += 1

                elif reaction.reaction_type == 2:

                    if post.dislike_count > 0:
                        post.dislike_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        post.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        post.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        post.sad_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        post.angry_count += 1

                elif reaction.reaction_type == 3:

                    if post.love_count > 0:
                        post.love_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        post.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        post.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        post.sad_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        post.angry_count += 1

                elif reaction.reaction_type == 4:

                    if post.sad_count > 0:

                        post.sad_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        post.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        post.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        post.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 5:
                        post.angry_count += 1

                elif reaction.reaction_type == 5:

                    if post.angry_count > 0:
                        post.angry_count -= 1

                    if serializer.validated_data["reaction_type"] == 1:
                        post.like_count += 1

                    elif serializer.validated_data["reaction_type"] == 2:
                        post.dislike_count += 1

                    elif serializer.validated_data["reaction_type"] == 3:
                        post.love_count += 1

                    elif serializer.validated_data["reaction_type"] == 4:
                        post.sad_count += 1

            post.save()
            reaction.reaction_type = serializer.validated_data["reaction_type"]
            reaction.save()

        else:
            if serializer.validated_data["reaction_type"] == 1:
                post.like_count += 1

            elif serializer.validated_data["reaction_type"] == 2:
                post.dislike_count += 1

            elif serializer.validated_data["reaction_type"] == 3:
                post.love_count += 1

            elif serializer.validated_data["reaction_type"] == 4:
                post.sad_count += 1

            elif serializer.validated_data["reaction_type"] == 5:
                post.angry_count += 1

            post.save()
            instance = serializer.save()

        context = {
            "reaction": instance.to_dict() if not reaction else reaction.to_dict(),
            "post": post.to_dict(),
        }
        return CustomResponse(data=context, message="added reaction succussfuly")

    def delete(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        serializer = s.ReactionPostSerializer(data=request.data)

        if not post:
            raise NotFoundException("this post does not exist")

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        reaction = m.PostReaction.objects.filter(
            post=post,
            user=request.user,
        ).first()

        if reaction is not None:

            if serializer.validated_data["reaction_type"] == 1:
                post.like_count -= 1

            elif serializer.validated_data["reaction_type"] == 2:
                post.dislike_count -= 1

            elif serializer.validated_data["reaction_type"] == 3:
                post.love_count -= 1

            elif serializer.validated_data["reaction_type"] == 4:
                post.sad_count -= 1

            elif serializer.validated_data["reaction_type"] == 5:
                post.angry_count -= 1

            reaction.delete()

            post.save()

        return CustomResponse(message="removed reaction succussfully")


class SavedPostAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        saved_post_data = m.SavedPost.objects.filter(user=request.user).all()

        saved_posts = [post.to_dict() for post in saved_post_data]

        context = {"posts": saved_posts}

        return CustomResponse(data=context, message="get saved posts")


class SavePostAPIView(APIView):

    permission_classes = [IsAuthenticated]  # IsBlockedPost]

    def post(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        if not post:
            raise NotFoundException("this post does not exist")

        instance = m.SavedPost.objects.create(user=request.user, post=post)

        context = {"saved_post": instance.to_dict()}

        return CustomResponse(data=context, message="saved post succussfuly")


class AddFilePostAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser,)

    def post(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id, user=request.user).first()

        if not post:
            raise NotFoundException("this post does not exist")

        validated_files = []
        for file in request.FILES.getlist("files"):

            serializer = s.PostFileSerializer(
                data={"file": file},
                context={"post": post, "file_type": file.content_type},
            )

            if not serializer.is_valid():
                raise BadRequestException(
                    message=serializer.error_messages, data=serializer.errors
                )

            instance = serializer.save()

            validated_files.append(instance)

        post.file.add(*validated_files)

        context = {"post": post.to_dict()}

        return CustomResponse(data=context, message="uploaded file to post ")


class SingleFilePostAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, post_id: int, file_id: int):

        post = m.Post.objects.filter(id=post_id, user=request.user).first()

        if not post:
            raise NotFoundException("this post does not exist")

        if not post.file:

            raise BadRequestException("no file uploaded to this post")

        file_instance: m.PostFile = post.file.filter(id=file_id).first()

        if not file_instance:
            raise NotFoundException("this file does not exist for this post")

        if file_instance.file:
            file_path = file_instance.file.path

            default_storage.delete(file_path)

        file_instance.delete()

        post.save()

        context = {"post": post.to_dict()}
        return CustomResponse(data=context, message="deleted file from post ")


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

        serializer = s.CommentSerializer(
            data=request.data, context={"post": post, "user": request.user}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        file_instance = None

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

        file_instance = file_serializer.save()

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

        file_instance = None

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

            file_instance = file_serializer.save()

        serializer = s.CommentSerializer(
            data=request.data, context={"comment": comment_data, "user": request.user}
        )

        if not serializer.is_valid():

            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        comment_data.text_content = serializer.validated_data["text_content"]

        if file_instance:
            comment_data.file = file_instance

        comment_data.save()

        context = {"comment": comment_data.to_dict()}

        return CustomResponse(data=context, message="updated comment on post")


class FriendsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        friends_data = m.Friends.objects.filter(user=request.user).all()

        friends = [friend.to_dict() for friend in friends_data]

        context = {"friends": friends}

        return CustomResponse(data=context, message="all user friends")

    def post(self, request: Request):

        serializer = s.UserSerializer(data=request.data)

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        if request.user.id == serializer.validated_data["id"]:

            raise BadRequestException("you cannot add  yourself as a friend")

        instance = m.Friends(user=request.data, friend=serializer.validated_data["id"])

        instance.save()

        context = {"friend": instance.to_dict()}

        return CustomResponse(data=context, message="added to friends successfully")


class ReportPostAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request):

        serializer = s.ReportPostSerializer(
            data=request.data, context={"user": request.user}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        report = m.ReportPost.objects.filter(
            post=serializer.validated_data["post"], user=request.user
        ).exists()

        if report:
            raise BadRequestException(message="you can only report a post once")

        serializer.save()

        return CustomResponse(message="reported post")


class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        friends_posts = m.Post.objects.filter(user__user_friends__friend=request.user)

        # additional posts from other users
        # additional_posts = m.Post.objects.exclude(user=request.user).order_by(
        #     "-created_at"
        # )[:5]

        post = friends_posts

        context = {"post": post}

        return CustomResponse(data=context, message="all post on user's feed")


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
