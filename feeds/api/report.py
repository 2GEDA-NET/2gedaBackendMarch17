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
