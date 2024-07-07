from fastapi import APIRouter, Response
from app.api.schemas.user import UserCreate, UserLogin
from app.core.security import get_current_user
from fastapi import Depends
from app.api.dependencies import users_service_dep, fingerprint_dep

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register")
async def register_user(user: UserCreate, users_service: users_service_dep):
    user = await users_service.register_user(user)
    return {"message": f"User {user.username} has been registered!"}


@auth_router.post("/login")
async def login_user(user: UserLogin, user_service: users_service_dep,
                     response: Response, fingerprint: fingerprint_dep):
    return await user_service.authenticate_user(user, response=response, fingerprint=fingerprint)


@auth_router.get("/me/")
def get_current_user_info(user: str = Depends(get_current_user)):
    return {"username": user}