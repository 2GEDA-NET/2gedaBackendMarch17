from rest_framework.exceptions import APIException
import rest_framework.status as status


class CustomException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class BadRequestException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, data=None, detail=None, code=None):

        self.message = message

        self.data = data

        super().__init__(detail, code)


class NotFoundException(CustomException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str, data=None, detail=None, code=None):

        self.message = message

        self.data = data

        super().__init__(detail, code)
