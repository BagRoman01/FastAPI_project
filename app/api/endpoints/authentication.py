from fastapi import APIRouter, Response
from app.api.schemas.user import UserCreate, UserLogin
from app.api.dependencies import (
    auth_service_dep,
    fingerprint_dep,
    tokens_dep
)

auth = APIRouter(prefix="/auth")


@auth.post("/register")
async def register_user(
        user: UserCreate,
        service_auth: auth_service_dep
):
    return await service_auth.register_user(user)


@auth.post("/login")
async def login_user(
        user: UserLogin,
        service_auth: auth_service_dep,
        response: Response,
        fingerprint: fingerprint_dep
):
    return await service_auth.authenticate_user(
        user,
        response=response,
        fingerprint=fingerprint
    )


@auth.post('/refresh')
async def refresh_tokens(
        response: Response,
        tokens: tokens_dep,
        fingerprint: fingerprint_dep,
        service_auth: auth_service_dep,
):
    return await service_auth.refresh_tokens(
        response,
        tokens,
        fingerprint
    )


@auth.get("/authorize")
async def authorize(
        service_auth: auth_service_dep,
        response: Response,
        fingerprint: fingerprint_dep,
        tokens: tokens_dep
):
    return await service_auth.authorize(
        response,
        tokens,
        fingerprint
    )

