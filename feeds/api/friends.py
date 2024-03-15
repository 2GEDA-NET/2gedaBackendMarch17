from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView


from utils.exception import BadRequestException
from utils.response import CustomResponse

from .. import models as m
from .. import serializers as s




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