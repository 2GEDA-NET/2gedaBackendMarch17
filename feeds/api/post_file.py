from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView


from utils.exception import BadRequestException, NotFoundException
from utils.response import CustomResponse

from .. import models as m
from .. import serializers as s





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
