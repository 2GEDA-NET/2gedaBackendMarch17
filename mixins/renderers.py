from rest_framework import mixins, status
from rest_framework.response import Response


class ListModelRenderer(mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )


class RetrieveModelRenderer(mixins.RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )


class CreateModelRenderer(mixins.CreateModelMixin):

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        return Response(
            {"message": "Created", "status": True, "data": data},
            status=status.HTTP_201_CREATED,
        )


class UpdateModelRenderer(mixins.CreateModelMixin):

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs).data
        return Response(
            {"message": "Updated", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        data = super().partial_update(request, *args, **kwargs).data
        return Response(
            {"message": "Updated", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )


class DestroyModelRenderer(mixins.CreateModelMixin):

    def destroy(self, request, *args, **kwargs):
        data = super().destroy(request, *args, **kwargs).data
        return Response(
            {"message": "Updated", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )


class ListCreateModelRenderer(CreateModelRenderer, ListModelRenderer):
    pass


class ListRetrieveCreateModelRenderer(
    CreateModelRenderer, ListModelRenderer, RetrieveModelRenderer
):
    pass


class CrudModelRenderer(
    CreateModelRenderer,
    ListModelRenderer,
    RetrieveModelRenderer,
    UpdateModelRenderer,
    DestroyModelRenderer,
):
    pass
