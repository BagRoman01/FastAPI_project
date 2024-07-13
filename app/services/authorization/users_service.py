from app.api.schemas.others import Tokens
from app.api.schemas.user import UserCreate, UserFromDb, UserLogin
from app.core.security import (
    hash_password,
    verify_pwd,
    create_jwt_token,
    create_session,
    set_tokens_to_cookies
)
from app.exceptions.auth_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    AuthenticationError
)
from app.services.authorization.sessions_service import SessionsService
from app.utils.uow import IUnitOfWork
from fastapi import Response


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register_user(self, user: UserCreate):
        async with self.uow:
            existing_user = await self.uow.user_repos.find_by_username(user.username)
            if existing_user:
                raise UserAlreadyExistsError(username=existing_user.username)
            hashed_pwd = await hash_password(user.password)
            user_dict = user.model_dump()
            user_dict["hashed_password"] = hashed_pwd
            del user_dict["password"]
            query_exec = await self.uow.user_repos.add_one(user_dict)
            result = UserFromDb.model_validate(query_exec)
            await self.uow.commit()
            return result

    async def get_user_from_db(
            self,
            user_id: int = None,
            username: str = None
    ) -> UserFromDb:
        async with self.uow:
            if user_id and username:
                raise ValueError("Both user_id and username cannot be specified simultaneously.")

            if user_id:
                user = await self.uow.user_repos.find_by_id(user_id)
            elif username:
                user = await self.uow.user_repos.find_by_username(username)

            if not user:
                raise UserNotFoundError

            user_from_db = UserFromDb(id=user.id, username=user.username, hashed_password=user.hashed_password)
            return user_from_db

    async def authenticate_user(
            self,
            user: UserLogin,
            response: Response,
            fingerprint: str
    ):
        async with self.uow:
            user_from_db: UserFromDb = await self.uow.user_repos.find_by_username(username=user.username)

            if not user_from_db:
                raise UserNotFoundError

            if not verify_pwd(user.password, user_from_db.hashed_password):
                raise AuthenticationError

            access_token = create_jwt_token(data={"username": user.username})
            new_session = create_session(user_from_db, fingerprint)

            session_service = SessionsService(self.uow)

            # явно выходим из первой сессии и закрываем ее
            await self.uow.__aexit__(None, None, None)

            added_session = await session_service.add_session(new_session)

            set_tokens_to_cookies(response, Tokens(access_token=access_token,
                                                   refresh_token=added_session.refresh_token))
            return {'access-token': access_token, "token-type": "Bearer"}