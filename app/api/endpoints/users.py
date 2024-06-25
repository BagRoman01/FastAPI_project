from sqlalchemy import select
from fastapi import APIRouter, status, HTTPException

from app.api.schemas.user import UserCreate
from app.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import bcrypt
from app.database.models.user import User

auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.post("/register/")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    found_user = await session.execute(select(User).where(User.username == user.username))
    existing_user = found_user.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists!"
        )

    hashed_pwd = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.model_dump()
    user_dict["hashed_password"] = user_dict.pop('password')
    user_dict["hashed_password"] = hashed_pwd
    user_to_register = User(**user_dict)
    session.add(user_to_register)
    await session.commit()
    return {"message": "You are registered!"}
