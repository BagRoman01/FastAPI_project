from fastapi import APIRouter, Response
from app.api.schemas.others import Tokens
from app.api.schemas.user import UserCreate, UserLogin
from app.core.security import (
    get_current_user,
    check_session,
    create_jwt_token,
    create_session,
    set_tokens_to_cookies
)
from app.api.dependencies import (
    users_service_dep,
    fingerprint_dep,
    sessions_service_dep,
    tokens_dep
)
from app.exceptions.token_exceptions import AccessTokenExpiredError

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register")
async def register_user(
        user: UserCreate,
        users_service: users_service_dep
):
    user = await users_service.register_user(user)
    return {"message": f"User {user.username} has been registered!"}


@auth_router.post("/login")
async def login_user(
        user: UserLogin,
        users_service: users_service_dep,
        response: Response,
        fingerprint: fingerprint_dep
):
    return await users_service.authenticate_user(user,
                                                 response=response,
                                                 fingerprint=fingerprint)


@auth_router.post('/refresh')
async def refresh_tokens(
        response: Response,
        tokens: tokens_dep,
        sessions_service: sessions_service_dep,
        users_service: users_service_dep,
        fingerprint: fingerprint_dep
):
    print(tokens.refresh_token)
    session = await sessions_service.get_session_by_refresh_token(tokens.refresh_token)
    user_id = check_session(session, fingerprint)
    user = await users_service.get_user_from_db(user_id)
    new_access_token = create_jwt_token(user.model_dump())
    print(new_access_token)
    new_session = create_session(user, fingerprint)
    new_refresh_token = new_session.refresh_token
    await sessions_service.add_session(new_session)
    print(f'new_access_token: {new_access_token}')
    print(f'new_refresh_token: {new_refresh_token}')

    set_tokens_to_cookies(response, Tokens(access_token=new_access_token,
                                           refresh_token=new_refresh_token))
    return Tokens(access_token=new_access_token, refresh_token=new_refresh_token)


@auth_router.get("/authorize")
async def authorize(
        response: Response, tokens: tokens_dep,
        sessions_service: sessions_service_dep,
        users_service: users_service_dep,
        fingerprint: fingerprint_dep):
    try:
        current_user: str = get_current_user(tokens.access_token)
        return {"message": f"{current_user} has been authorized."}
    except AccessTokenExpiredError:
        new_tokens = await refresh_tokens(response, tokens, sessions_service, users_service, fingerprint)
        current_user: str = get_current_user(new_tokens.access_token)
        print('АВТОРИЗАЦИЯ ЗА СЧЕТ НОВОГО ТОКЕНА ДОСТУПА')
    return current_user

