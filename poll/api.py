from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from mixins import renderers

from . import models as m
from . import serializers as s
from .permissions import IsPollCreatorPermission


class PollsAPI(renderers.ReadOnlyModelRenderer, viewsets.GenericViewSet):

    serializer_class = s.PollSerializer
    queryset = m.Poll.objects.all()
    lookup_url_kwarg = "poll_id"

    params = [openapi.Parameter("find", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)]

    def get_permissions(self):
        if self.action == "vote":
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == "vote":
            return s.WriteOnlyPollOptionSerializer
        return s.PollSerializer

    @decorators.action(methods=["GET"], detail=False, url_path="paid")
    def paid(self, request, *args, **kwargs):
        active_polls = m.Poll.objects.filter(is_paid=True)
        data = s.PollSerializer(active_polls, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=False, url_path="suggested")
    def suggested(self, request, *args, **kwargs):
        active_polls = m.Poll.objects.all()
        data = s.PollSerializer(active_polls, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=False, url_path="promoted")
    def promoted(self, request, *args, **kwargs):
        active_polls = m.Poll.objects.all()
        data = s.PollSerializer(active_polls, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(method="GET", manual_parameters=params)
    @decorators.action(methods=["GET"], detail=False, url_path="find")
    def find(self, request, *args, **kwargs):
        query = request.query_params.get("find", "")
        if query:
            active_polls = m.Poll.objects.filter(question__icontains=query)
        else:
            active_polls = m.Poll.objects.none()
        data = s.PollSerializer(active_polls, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["POST"], detail=True, url_path="vote")
    def vote(self, request, *args, **kwargs):
        poll_id = kwargs.get("poll_id", 0)
        option_id = request.data.get("option_id", 0)
        profile = request.user.profile
        # print("Poll DI: ", poll_id)
        poll = m.Poll.objects.filter(pk=int(poll_id))
        if poll.exists():
            poll = poll.first()
            # check if user have voted for the actual poll alredy
            if profile in poll.voters.all():
                return Response(
                    {"message": "You have voted already!", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                # user can not vote for he/her own poll
            if poll.creator == profile:
                return Response(
                    {"message": "You can't vote for your poll!", "status": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            option = m.PollOption.objects.filter(pk=int(option_id), poll=poll)
            if option.exists():
                # add user to the options he/she voted for
                option.first().voters.add(profile)
                # add user to the actual poll
                # whether he/she has voted so to keep track/record
                poll.voters.add(profile)
                return Response(
                    {"message": "Voted!", "status": True}, status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Invalid Option!", "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Invalid Poll!", "status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserPollAPI(renderers.CrudModelRenderer, viewsets.GenericViewSet):

    # permission_classes = [IsAuthenticated, IsPollCreatorPermission]
    lookup_url_kwarg = "poll_id"
    serializer_class = s.PollSerializer

    params = [openapi.Parameter("find", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)]

    def get_permissions(self):
        if self.action == "create":
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated, IsPollCreatorPermission]
        return [permission() for permission in permissions]

    def get_queryset(self):
        return m.Poll.objects.filter(creator=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.profile)

    @decorators.action(methods=["GET"], detail=False, url_path="active")
    def active(self, request, *args, **kwargs):
        active_polls = m.Poll.objects.filter(
            creator=request.user.profile, is_closed=False
        )
        data = s.PollSerializer(active_polls, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=False, url_path="ended")
    def ended(self, request, *args, **kwargs):
        active_polls = m.Poll.objects.filter(
            creator=request.user.profile, is_closed=True
        )
        data = s.PollSerializer(active_polls, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=True, url_path="close")
    def close(self, request, *args, **kwargs):
        poll_id = kwargs.get("poll_id", 0)
        poll = m.Poll.objects.filter(pk=int(poll_id))
        if poll.exists():
            poll.update(is_closed=True)
            return Response(
                {"message": "Poll closed!", "status": True}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Invalid Poll!", "status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(method="GET", manual_parameters=params)
    @decorators.action(methods=["GET"], detail=False, url_path="find")
    def find(self, request, *args, **kwargs):
        query = request.query_params.get("find", "")
        if query:
            active_polls = m.Poll.objects.filter(
                creator=request.user.profile, question__icontains=query
            )
        else:
            active_polls = m.Poll.objects.none()
        data = s.PollSerializer(active_polls, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )
