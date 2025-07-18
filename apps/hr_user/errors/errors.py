from http import HTTPStatus
from typing import Optional

from apps.hr_user.errors.error_codes import HRUserErrorCodes
from rest_framework.exceptions import APIException


class AccountDoesNotExist(APIException):
    def __init__(
        self, message: Optional[str] = None, status_code: Optional[str] = None, error_code: Optional[int] = None
    ):
        self.message = message or "Kullanıcı bulunamadı."
        self.status_code = status_code or HTTPStatus.NOT_FOUND
        self.error_code = error_code or HRUserErrorCodes.DOES_NOT_EXISTS
