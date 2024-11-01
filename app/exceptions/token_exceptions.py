from fastapi import HTTPException
from starlette import status


class InvalidAccessTokenError(HTTPException):
    def __init__(
            self,
            detail: str = "Invalid access token",
            status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class InvalidRefreshTokenError(HTTPException):
    def __init__(
            self,
            detail: str = "Invalid refresh token",
            status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)


class NoFingerprintMatchError(HTTPException):
    def __init__(
            self,
            detail: str = "Fingerprints don't match!",
            status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)


class NoInfoAccessTokenError(HTTPException):
    def __init__(
            self,
            detail: str = "Access token doesn't contain user information",
            status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class AccessTokenExpiredError(HTTPException):
    def __init__(
            self,
            detail: str = "Access token has expired",
            status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)


class RefreshTokenExpiredError(HTTPException):
    def __init__(
            self,
            detail: str = "Refresh token has expired",
            status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)


class AccessTokenNotFoundError(HTTPException):
    def __init__(
            self,
            detail: str = "Access token has not been found!",
            status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)


class RefreshTokenNotFoundError(HTTPException):
    def __init__(
            self,
            detail: str = "Refresh token has not been found!",
            status_code: int = status.HTTP_404_NOT_FOUND
    ):
        super().__init__(status_code=status_code, detail=detail)




