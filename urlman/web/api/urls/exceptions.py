from fastapi import HTTPException


class UrlNotFoundException(HTTPException):
    """Raised url user is not founded."""

    def __init__(self) -> None:
        super(UrlNotFoundException, self).__init__(
            status_code=404,
            detail="URL not found.",
        )


class UrlKeyMatchingException(HTTPException):
    """Raised when url key are wrong."""

    def __init__(self) -> None:
        super(UrlKeyMatchingException, self).__init__(
            status_code=400,
            detail="Wrong URL key.",
        )
