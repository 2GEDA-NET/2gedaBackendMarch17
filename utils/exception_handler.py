# https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
from rest_framework.response import Response
from rest_framework.views import exception_handler
from .exception import NotFoundException, BadRequestException
from .response import CustomResponse


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, (NotFoundException, BadRequestException)):

        response = CustomResponse(
            data=exc.data, message=exc.message, success=False, status=exc.status_code
        )

        return response

    # Now add the HTTP status code to the response.
    if response is not None:
        detail = response.data.get("detail")
        message = response.data.get("message")
        data = {"status": False}
        if detail or message:
            data["message"] = detail or message
        else:
            data["message"] = "Validation error!"
            data["data"] = response.data
        return Response(data, status=response.status_code)
    return None
