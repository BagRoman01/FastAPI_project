import asyncio
from datetime import timedelta, datetime, timezone, UTC
from secrets import token_hex
import jwt
from passlib.context import CryptContext
from app.api.schemas.tokens import Tokens
from app.api.schemas.session import SessionCreate, Session
from app.api.schemas.user import UserFromDb
from app.core.config import settings
from fastapi import Response, Request
from app.exceptions.token_exceptions import (
    InvalidAccessTokenError,
    NoInfoAccessTokenError,
    AccessTokenExpiredError,
    TokensNotFoundError,
    InvalidRefreshTokenError,
    RefreshTokenExpiredError
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(pwd_context.hash, password)


def verify_pwd(
        password: str,
        hashed_pwd: str
) -> bool:
    return pwd_context.verify(password, hashed_pwd)


def create_jwt_token(
        data: dict,
        expires_delta: timedelta = None
):
    to_encode = data.copy()
    time_now = datetime.now(UTC)
    expire = time_now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_session(
        user: UserFromDb,
        fingerprint: str
):
    create_date = datetime.now(timezone.utc)

    refresh_token = token_hex(8)

    session = SessionCreate(
        refresh_token=refresh_token,
        fingerprint=fingerprint,
        user_id=user.id,
        exp_at=create_date + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        created_at=create_date
    )
    return session


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AccessTokenExpiredError()

    except jwt.InvalidTokenError:
        raise InvalidAccessTokenError()


def get_current_user(token: str):
    payload = decode_access_token(token)
    if "username" not in payload:
        raise NoInfoAccessTokenError()
    return payload["username"]


def set_refresh_token_to_cookie(
        response: Response,
        refresh_token: str,
):
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True
    )


def get_fingerprint(request: Request):
    return str(request.headers.get('user-agent'))


def get_refresh_token_from_cookie(request: Request):
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        return refresh_token
    raise TokensNotFoundError


def check_session(
        session: Session,
        fingerprint: str
):
    if not session:
        raise InvalidRefreshTokenError

    if session.fingerprint != fingerprint:
        raise InvalidRefreshTokenError

    if session.exp_at <= datetime.now(timezone.utc):
        raise RefreshTokenExpiredError

    return session.user_id

