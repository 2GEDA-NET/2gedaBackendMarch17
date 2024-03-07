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

# from .permissions impor] #IsBlockedPost


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

        if post.file:
            raise BadRequestException("File already exists for this post")

        serializer = s.PostFileSerializer(
            data=request.data,
            context={
                "post": post,
                "file_type": request.data["file"].content_type,
            },
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        instance = serializer.save()

        post.file = instance

        post.save()

        context = {"post": post.to_dict()}

        return CustomResponse(data=context, message="uploaded file to post ")

    def delete(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id, user=request.user).first()

        if not post:
            raise NotFoundException("this post does not exist")

        if not post.file:

            raise BadRequestException("no file uploaded to this post")

        post.file.delete()

        post.file = None
        post.save()

        context = {"post": post.to_dict()}
        return CustomResponse(data=context, message="deleted file from post ")


class CommentPostAPIView(APIView):

    permission_classes = [IsAuthenticated]  # IsBlockedPost]

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

        instance = serializer.save()

        context = {"comment": instance.to_dict()}

        return CustomResponse(
            data=context, message="created comment on post succussfuly"
        )


# class SingleCommentAPIView(APIView):

#     permission_classes = [IsAuthenticated] #IsBlockedPost]

#     def patch(self, request: Request, post_id: int, comment_id: int):

#         comment_data = Comment.objects.filter(
#             id=comment_id, post=post_id, user=request.user
#         ).first()

#         if comment_id:
#             raise NotFoundException("this comment does mno ")

#         serializer = CommentSerializer(
#             data=request.data, context={"post": post, "user": request.user}
#         )

#         context = {"comments": comments}

#         return CustomResponse(data=context, message="get posts comments")

#     pass
