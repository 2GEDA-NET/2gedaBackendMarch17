from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView


from utils.exception import BadRequestException, NotFoundException
from utils.response import CustomResponse

from .. import models as m
from .. import serializers as s
from .. import mime_types as mime
from ..permissions import IsBlockedPost




class PostAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        if request.query_params.get("filter"):

            param = request.query_params.get("filter")

            if param not in [
                "image",
                "video",
                "audio",
                "file",
                "other",
                "location",
                "all",
            ]:
                raise BadRequestException("invalid query params for filter")

            if param == "image":
                filtered_posts = m.Post.objects.filter(
                    user=request.user, file__file_type__in=mime.image_types
                )

                serialized_posts = [post.to_dict() for post in filtered_posts]

            elif param == "video":

                filtered_posts = m.Post.objects.filter(
                    user=request.user, file__file_type__in=mime.video_types
                )

                serialized_posts = [post.to_dict() for post in filtered_posts]

            elif param == "music":

                filtered_posts = m.Post.objects.filter(
                    user=request.user, file__file_type__in=mime.music_types
                )

                serialized_posts = [post.to_dict() for post in filtered_posts]

            elif param == "voice_note":

                filtered_posts = m.Post.objects.filter(
                    user=request.user, file__file_type__in=mime.voice_note_types
                )


            elif param == "file":

                filtered_posts = m.Post.objects.filter(
                    user=request.user, file__file_type__in=mime.document_types
                )

                serialized_posts = [post.to_dict() for post in filtered_posts]

            elif param == "location":
                filtered_posts = m.Post.objects.filter(
                    user=request.user, location__isnull=False
                )

                serialized_posts = [post.to_dict() for post in filtered_posts]

            elif param == "other":
                filtered_posts = m.Post.objects.filter(
                    user=request.user, file__file_type__in=mime.other_types
                )

                serialized_posts = [post.to_dict() for post in filtered_posts]

            elif param == "all":

                filtered_posts = m.Post.objects.filter(user=request.user).all()

                serialized_posts = [post.to_dict() for post in filtered_posts]

            return CustomResponse(data=serialized_posts, message="get user's posts")

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

    permission_classes = []

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

        
        reactions = m.PostReaction.objects.filter(post=post).all()        

        if not post:
            raise NotFoundException("this post does not exist")

        context = {
            "user_reactions": [reaction.to_user_reaction() for reaction in reactions],
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







class RepostView(APIView):

    permission_classes = [IsAuthenticated, IsBlockedPost]

    def post(self, request: Request, post_id: int):

        post = m.Post.objects.filter(id=post_id).first()

        if post is None:
            raise NotFoundException("this post does not exist")

        serializer = s.RepostSerializer(
            data=request.data,
            context={
                "user": request.user,
                "post": post,
                "text_content": request.data.get("text_content"),
            },
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        instance = serializer.save()

        context = {"post": instance.to_dict()}

        return CustomResponse(data=context, message="created repost succussfuly")
    




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








