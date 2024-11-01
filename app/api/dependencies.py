from typing import Annotated
from api.schemas.tokens import Tokens
from app.core.security import get_fingerprint
from app.services.authorization.auth_service import AuthService
from fastapi import Depends, Request
from app.services.currency.currency_service import CurrencyService
from fastapi.security import OAuth2PasswordBearer
from exceptions.token_exceptions import AccessTokenNotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def getTokens(request: Request, access_token: str = Depends(oauth2_scheme)) -> Tokens:
    refresh_token = getRefresh(request)
    if not access_token:
        raise AccessTokenNotFoundError
    return Tokens(access_token=access_token, refresh_token=refresh_token)


def getRefresh(request: Request):
    return request.cookies.get('refresh_token')


fingerprint_dep = Annotated[str, Depends(get_fingerprint)]
auth_service_dep = Annotated[AuthService, Depends(AuthService)]
tokens_dep = Annotated[Tokens, Depends(getTokens)]
refresh_dep = Annotated[str, Depends(getRefresh)]
access_token_dep = Annotated[str, Depends(oauth2_scheme)]
currency_service_dep = Annotated[CurrencyService, Depends(CurrencyService)]

