from datetime import timedelta
from sqlalchemy import select
from fastapi import APIRouter, status, HTTPException, Response
from app.api.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_pwd, create_jwt_token, get_current_user, set_token_to_cookies
from app.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.models.user import User
from app.utils.exceptions import UserAlreadyExists, RegistrationException, UserNotFoundError, AuthenticationError

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register/")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    found_user = await session.execute(select(User).where(User.username == user.username))
    existing_user = found_user.scalar_one_or_none()
    if existing_user:
        await session.rollback()
        raise UserAlreadyExists()

    hashed_pwd = await hash_password(user.password)
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hashed_pwd
    del user_dict["password"]
    user_to_register = User(**user_dict)
    session.add(user_to_register)
    await session.commit()
    return {"message": "You are registered!"}


@auth_router.post("/login/")
async def login_user(response: Response, user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    found_user = await session.execute(select(User).where(User.username == user.username))
    existing_user = found_user.scalar_one_or_none()

    if not existing_user:
        raise UserNotFoundError()

    if not verify_pwd(user.password, existing_user.hashed_password):
        raise AuthenticationError()

    access_token = create_jwt_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )

    set_token_to_cookies(response, access_token)
    return {"access-token": access_token, "token-type": "Bearer"}


@auth_router.get("/me/")
def get_current_user_info(user: str = Depends(get_current_user)):
    return {"username": user}