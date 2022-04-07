from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    """Raised when user is not founded."""

    def __init__(self) -> None:
        super(UserNotFoundException, self).__init__(
            status_code=404,
            detail="User not found.",
        )


class UserNotProvidedException(HTTPException):
    """Raised when user token is invalid."""

    def __init__(self) -> None:
        super(UserNotProvidedException, self).__init__(
            status_code=401,
            detail="User not provided.",
        )


class UserCredentialsException(HTTPException):
    """Raised when users credentials are wrong."""

    def __init__(self) -> None:
        super(UserCredentialsException, self).__init__(
            status_code=401,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserPasswordMismatchException(HTTPException):
    """Raised when password don't match."""

    def __init__(self) -> None:
        super(UserPasswordMismatchException, self).__init__(
            status_code=400,
            detail="Passwords don't match",
        )
