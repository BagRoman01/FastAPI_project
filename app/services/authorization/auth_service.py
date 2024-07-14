from typing import Annotated
from fastapi import Depends
from app.api.schemas.tokens import Tokens
from app.api.schemas.user import UserLogin, UserCreate
from app.core.security import (
    verify_pwd,
    create_jwt_token,
    create_session,
    set_tokens_to_cookies, check_session, get_current_user
)
from app.exceptions.auth_exceptions import AuthenticationError
from app.exceptions.token_exceptions import AccessTokenExpiredError
from app.services.authorization.sessions_service import SessionsService
from app.services.authorization.users_service import UsersService
from fastapi import Response
from app.utils.uow import UnitOfWork, IUnitOfWork

i_uow_dep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


class AuthService:
    def __init__(self, uow: i_uow_dep):
        self.session_service = SessionsService(uow)
        self.user_service = UsersService(uow)

    async def register_user(self, user: UserCreate):
        user = await self.user_service.register_user(user)
        return {"message": f"User {user.username} has been registered!"}

    async def authenticate_user(
            self,
            user: UserLogin,
            response: Response,
            fingerprint: str
    ):
        user_from_db = await self.user_service.get_user_from_db(username=user.username)

        if not verify_pwd(user.password, user_from_db.hashed_password):
            raise AuthenticationError

        access_token = create_jwt_token(data={"username": user.username})
        new_session = create_session(user_from_db, fingerprint)
        added_session = await self.session_service.add_session(new_session)

        set_tokens_to_cookies(response, Tokens(access_token=access_token,
                                               refresh_token=added_session.refresh_token))
        return {'access-token': access_token}

    async def refresh_tokens(
            self,
            response: Response,
            tokens: Tokens,
            fingerprint: str
    ):
        session = await self.session_service.get_session_by_refresh_token(tokens.refresh_token)
        user_id = check_session(session, fingerprint)
        user = await self.user_service.get_user_from_db(user_id)
        new_access_token = create_jwt_token(user.model_dump())
        new_session = create_session(user, fingerprint)
        await self.session_service.delete_session(session.id)
        new_refresh_token = new_session.refresh_token
        await self.session_service.add_session(new_session)

        set_tokens_to_cookies(response, Tokens(access_token=new_access_token,
                                               refresh_token=new_refresh_token))
        return Tokens(access_token=new_access_token, refresh_token=new_refresh_token)

    async def authorize(
            self,
            response: Response,
            tokens: Tokens,
            fingerprint: str
    ):
        try:
            current_user: str = get_current_user(tokens.access_token)
        except AccessTokenExpiredError:
            new_tokens = await self.refresh_tokens(response, tokens, fingerprint)
            current_user: str = get_current_user(new_tokens.access_token)
        return current_user

