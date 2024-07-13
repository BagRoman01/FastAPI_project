from fastapi import APIRouter, Response
from app.api.schemas.user import UserCreate, UserLogin

from app.api.dependencies import (
    auth_service_dep,
    fingerprint_dep,
    tokens_dep
)

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register")
async def register_user(
        user: UserCreate,
        service_auth: auth_service_dep
):
    return await service_auth.register_user(user)


@auth_router.post("/login")
async def login_user(
        user: UserLogin,
        service_auth: auth_service_dep,
        response: Response,
        fingerprint: fingerprint_dep
):
    return await service_auth.authenticate_user(user,
                                                response=response,
                                                fingerprint=fingerprint)


@auth_router.post('/refresh')
async def refresh_tokens(
        response: Response,
        tokens: tokens_dep,
        fingerprint: fingerprint_dep,
        service_auth: auth_service_dep
):
    return await service_auth.refresh_tokens(response, tokens, fingerprint)


@auth_router.get("/authorize")
async def authorize(
        service_auth: auth_service_dep,
        response: Response,
        tokens: tokens_dep,
        fingerprint: fingerprint_dep
):
    return await service_auth.authorize(response, tokens, fingerprint)

