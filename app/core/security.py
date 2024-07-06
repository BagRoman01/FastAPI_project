import asyncio
from datetime import timedelta, datetime, timezone
from secrets import token_hex
import jwt
from jose import JWTError
from passlib.context import CryptContext
from app.api.schemas.others import Tokens
from app.api.schemas.session import SessionCreate
from app.api.schemas.user import UserFromDb
from app.core.config import settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import Response, Request
from app.services.exceptions import InvalidTokenError, NoInfoTokenError, TokenExpiredError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(pwd_context.hash, password)


def verify_pwd(password: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(password, hashed_pwd)


def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    time_now = datetime.now(timezone.utc)
    expire = time_now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_session(user: UserFromDb, fingerprint: str):
    create_date = datetime.now()
    refresh_token = token_hex(8)

    session = SessionCreate(
        refresh_token=refresh_token,
        fingerprint=fingerprint,
        user_id=user.id,
        exp_at=create_date.timestamp() + settings.refresh_exp,
        created_at=create_date
    )
    return session


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise InvalidTokenError()


def get_token_from_cookie(request: Request):
    return request.cookies.get("access-token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise TokenExpiredError()

    payload = decode_access_token(token)
    if "sub" not in payload:
        raise NoInfoTokenError()
    return payload["sub"]


def set_tokens_to_cookies(response: Response, tokens: Tokens):
    response.set_cookie('access_token', tokens.access_token, httponly=True)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)
    return response


def get_fingerprint(request: Request):
    return str(request.headers.get('user-agent'))
