from http.client import HTTPException
from typing import Annotated
from fastapi import Depends

from app.api.schemas.tokens import Tokens
from app.api.schemas.user import UserLogin, UserCreate
from app.core.security import (
    verify_pwd,
    create_jwt_token,
    create_session,
    set_refresh_token_to_cookie,
    check_session,
    get_current_user
)
from app.exceptions.auth_exceptions import AuthenticationError, SessionNotFoundError
from app.exceptions.token_exceptions import AccessTokenExpiredError
from app.services.authorization.sessions_service import SessionsService
from app.services.authorization.users_service import UsersService
from fastapi import Response, Request
from app.utils.uow import UnitOfWork, IUnitOfWork

i_uow_dep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


class AuthService:
    def __init__(self, uow: i_uow_dep):
        self.session_service = SessionsService(uow)
        self.user_service = UsersService(uow)

    async def register_user(self, user: UserCreate):
        user = await self.user_service.register_user(user)
        return {"username": user.username}

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

        set_refresh_token_to_cookie(response=response, refresh_token=added_session.refresh_token)
        return {"access_token": access_token, "token_type": "bearer"}

    async def refresh_tokens(
            self,
            response: Response,
            refresh_token: str,
            fingerprint: str
    ):
        session = await self.session_service.get_session_by_refresh_token(refresh_token)
        user_id = check_session(session, fingerprint)
        user = await self.user_service.get_user_from_db(user_id)
        new_access_token = create_jwt_token(user.model_dump())
        new_session = create_session(user, fingerprint)
        await self.session_service.delete_session(session.id)
        new_refresh_token = new_session.refresh_token
        await self.session_service.add_session(new_session)

        set_refresh_token_to_cookie(refresh_token=new_refresh_token, response=response)
        return {"access_token": new_access_token, "token_type": "bearer"}

    @staticmethod
    async def authorize(
            tokens: Tokens
    ):
        try:
            current_user: str = get_current_user(tokens.access_token)
        except HTTPException as e:
            raise e

        return current_user

    async def logout(
            self,
            response: Response,
            request: Request,
            fingerprint: str
    ):

        refresh_token = request.cookies.get('refresh_token')
        result = await self.session_service.delete_session_by_refresh_token_and_fingerprint(
            refresh_token,
            fingerprint
        )
        response.delete_cookie('refresh_token')
        return result
