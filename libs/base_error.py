from typing import Optional


class APIException(Exception):
    def __init__(
        self, message: Optional[str] = None, status_code: Optional[str] = None, error_code: Optional[int] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
