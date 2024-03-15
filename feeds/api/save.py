from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView


from utils.exception import NotFoundException
from utils.response import CustomResponse

from .. import models as m



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

