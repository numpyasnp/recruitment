from http import HTTPStatus
from typing import Optional

from rest_framework.exceptions import APIException

from apps.job_posting.errors.error_codes import JobPostingErrorCodes


class PermissionDenied(APIException):
    def __init__(
        self, message: Optional[str] = None, status_code: Optional[str] = None, error_code: Optional[int] = None
    ):
        self.message = message or "Bu işlem için izniniz bulunmuyor."
        self.status_code = status_code or HTTPStatus.FORBIDDEN
        self.error_code = error_code or JobPostingErrorCodes.PERMISSION_DENIED
