from fastapi import HTTPException
from starlette import status


class UserAlreadyExists(HTTPException):
    def __init__(self, username: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=f"User with username '{username}' already exists.")


class RegistrationException(HTTPException):
    def __init__(self, detail: str = "Registration failed. Please try again.",
                 status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundError(HTTPException):
    def __init__(self, detail: str = "User not found!", status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail=detail)


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Login or password is not valid", status_code: int = status.HTTP_403_FORBIDDEN):
        super().__init__(status_code=status_code, detail=detail)


class InvalidTokenError(HTTPException):
    def __init__(self, detail: str = "Invalid token", status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class NoInfoTokenError(HTTPException):
    def __init__(self, detail: str = "Token doesn't contain user information",
                 status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class TokenExpiredError(HTTPException):
    def __init__(self, detail: str = "Access token has expired", status_code: int = status.HTTP_403_FORBIDDEN):
        super().__init__(status_code=status_code, detail=detail)








