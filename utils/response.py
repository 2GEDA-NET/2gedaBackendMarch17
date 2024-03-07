import rest_framework.status as status_codes
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(
        self,
        data=None,
        message: str = "",
        success: bool = True,
        status=status_codes.HTTP_200_OK,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        response = {
            "status": success,
            "message": message,
            "data": data,
        }

        super().__init__(
            data=response,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
