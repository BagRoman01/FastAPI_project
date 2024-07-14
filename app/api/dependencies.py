from typing import Annotated
from app.api.schemas.tokens import Tokens
from app.core.security import get_fingerprint, get_tokens_from_cookie
from app.services.authorization.auth_service import AuthService
from fastapi import Depends
from app.services.currency.currency_service import CurrencyService

fingerprint_dep = Annotated[str, Depends(get_fingerprint)]
auth_service_dep = Annotated[AuthService, Depends(AuthService)]
tokens_dep = Annotated[Tokens, Depends(get_tokens_from_cookie)]
currency_service_dep = Annotated[CurrencyService, Depends(CurrencyService)]

