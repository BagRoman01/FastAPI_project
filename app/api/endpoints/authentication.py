from fastapi import APIRouter, Response, Request
from app.api.schemas.user import UserCreate, UserLogin
from app.api.dependencies import (
    auth_service_dep,
    fingerprint_dep,
    tokens_dep,
    refresh_dep
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
    print(user.username)
    print(user.password)
    return await service_auth.authenticate_user(
        user,
        response=response,
        fingerprint=fingerprint
    )


@auth.get('/refresh')
async def refresh_tokens(
        response: Response,
        refresh_token: refresh_dep,
        fingerprint: fingerprint_dep,
        service_auth: auth_service_dep,
):
    print(refresh_token)
    return await service_auth.refresh_tokens(
        response,
        refresh_token,
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


@auth.post("/logout")
async def logout(
    service_auth: auth_service_dep,
    response: Response,
    request: Request,
    fingerprint: fingerprint_dep
):
    return await service_auth.logout(
        response,
        request,
        fingerprint
    )
