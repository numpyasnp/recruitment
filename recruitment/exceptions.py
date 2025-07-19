from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from libs.base_error import APIException


def custom_exception_handler(exc, context):
    if isinstance(exc, APIException):
        response_data = {"error_code": exc.error_code, "message": exc.message, "status_code": exc.status_code}
        return Response(response_data, status=exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {"error_code": "server_error", "message": str(exc), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
