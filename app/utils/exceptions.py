from fastapi import HTTPException


class UserAlreadyExists(HTTPException):
    def __init__(self, detail: str = "User already exists!", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class RegistrationException(HTTPException):
    def __init__(self, detail: str = "Registration failed. Please try again.", status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundError(HTTPException):
    def __init__(self, detail: str = "User not found!", status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Login or password is not valid", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class InvalidTokenError(HTTPException):
    def __init__(self, detail: str = "Invalid token", status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class NoInfoTokenError(HTTPException):
    def __init__(self, detail: str = "Token doesn't contain user information", status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class TokenExpiredError(HTTPException):
    def __init__(self, detail: str = "Access token has expired", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)








