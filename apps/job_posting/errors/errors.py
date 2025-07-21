from http import HTTPStatus
from typing import Optional

from django.utils.translation import gettext_lazy as _

from apps.job_posting.errors.error_codes import JobPostingErrorCodes
from libs.base_error import APIException


class PermissionDenied(APIException):
    def __init__(
        self, message: Optional[str] = None, status_code: Optional[str] = None, error_code: Optional[int] = None
    ):
        self.message = message or _("You do not have permission for this action.")
        self.status_code = status_code or HTTPStatus.FORBIDDEN
        self.error_code = error_code or JobPostingErrorCodes.PERMISSION_DENIED
