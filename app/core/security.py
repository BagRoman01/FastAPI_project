import asyncio
from datetime import timedelta, datetime, timezone
import jwt
from jose import JWTError
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import HTTPException,Depends
from starlette import status
from fastapi.security import OAuth2PasswordBearer

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

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    except Exception as e:
        print(f"Error encoding JWT token: {e}")
        return None


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        # If there's an error decoding, raise an HTTP 401 (Unauthorized)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token doesn't contain user information",
            headers={"WWW-Authenticate": "Bearer"}
        )
        # Return the subject, which typically represents the user ID or username
    return payload["sub"]