from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView


from utils.exception import BadRequestException, NotFoundException
from utils.response import CustomResponse

from .. import models as m
from .. import serializers as s
from payments.requests import PaystackClient, params, IntializeTransactionResponse


class PromotePostView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        promoted_posts = m.PromotedPost.objects.filter(user=request.user).all()

        context = {
            "promoted_posts": [
                promoted_post.to_dict() for promoted_post in promoted_posts
            ]
        }

        return CustomResponse(data=context, message="all promotion plans")

    def post(self, request: Request):

        if type(request.data["post"]) is not int:
            raise BadRequestException(f"post is a valid int or pk value")

        post = m.Post.objects.filter(id=request.data["post"], user=request.user).first()

        if post is None:
            raise NotFoundException("this post does not exist")

        if m.PromotedPost.objects.filter(post=post).filter().exists():
            raise BadRequestException(
                "There is an active promoted plan on this post, please wait after the validity period"
            )

        serializer = s.PromotePostSerializer(
            data=request.data, context={"user": request.user, "post": post}
        )

        if not serializer.is_valid():
            raise BadRequestException(
                message=serializer.error_messages, data=serializer.errors
            )

        plan_amount = {
            m.PromotedPost.BASIC: 1000,
            m.PromotedPost.STANDARD: 5000,
            m.PromotedPost.PREMIUM: 9000,
            m.PromotedPost.PRO: 24000,
        }

        promotion_plain_amount = plan_amount.get(
            serializer.validated_data["plan"], 1000
        )

        promote_post_data = dict(serializer.validated_data)

        promote_post_data.update({"post": post.id, "user": request.user.id})

        transaction_initializer = params.PromotionPlanIntializeTransaction(
            email=request.user.email,
            amount=promotion_plain_amount,
            metadata=params.PromotionPlanMetaData(**promote_post_data),
        )

        client = PaystackClient()

        response = IntializeTransactionResponse(
            **client.initialize_transaction(transaction_initializer)
        )

        context = {"payment_url": response.data.authorization_url}

        return CustomResponse(
            data=context, message="promotion plan initialized succussfuly"
        )
