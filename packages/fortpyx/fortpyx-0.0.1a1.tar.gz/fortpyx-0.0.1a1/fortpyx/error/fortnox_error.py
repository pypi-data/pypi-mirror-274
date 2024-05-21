from typing import Optional


class FortnoxError(Exception):
    """See https://www.fortnox.se/developer/guides-and-good-to-know/errors"""

    def __init__(
        self,
        message: str,
        error_code: Optional[int] = None,
        original_exception: Optional[Exception] = None,
    ):
        super(Exception, self).__init__(message, original_exception)
        self.error_code = error_code
        self.description = message
