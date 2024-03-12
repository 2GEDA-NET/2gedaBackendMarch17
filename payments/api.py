import json
import hmac
import hashlib
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from pprint import pprint
from .requests.models import WebhookPayload
from feeds.models import PromotedPost, Post
from utils.exception import BadRequestException
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from . import models as m

User = get_user_model()


class PaystackWebhookView(APIView):
    permission_classes = []

    def post(self, request: Request):

        secret_key: str = settings.PAYSTACK_SECRET_KEY

        signature = request.headers.get("X-Paystack-Signature")

        hash_signature = hmac.new(
            secret_key.encode("utf-8"),
            request.body,
            hashlib.sha512,
        ).hexdigest()

        if not (hash_signature == signature):

            return Response(status=status.HTTP_403_FORBIDDEN)

        # Do something with the event
        event = WebhookPayload(**request.data)

        if event.event == "charge.success":

            if event.data.metadata.get("type") == "promote_post":

                user = User.objects.filter(id=int(event.data.metadata["user"])).first()
                post = Post.objects.filter(id=int(event.data.metadata["post"])).first()

                print(f"Post Promoted: {post}")
                promoted_post_instance = PromotedPost.objects.create(
                    post=post,
                    description=event.data.metadata["description"],
                    user=user,
                    plan=event.data.metadata["plan"],
                )

                print(f"Promoted Post is created: {promoted_post_instance}")

                payment_transaction = m.PaymentTransaction.objects.create(
                    user=promoted_post_instance.user,
                    payment_method="paystack",
                    amount=event.data.amount,
                    transaction_fee=(event.data.fees / 100),
                    status="success",
                )

                paystack_transaction = m.PaystackTransaction.objects.create(
                    transaction=payment_transaction,
                    amount=event.data.amount,
                    reference=event.data.reference,
                    fee=(event.data.fees / 100),
                )

                print(f"Payment Transaction is created: {paystack_transaction}")

        return Response(status=status.HTTP_200_OK)
