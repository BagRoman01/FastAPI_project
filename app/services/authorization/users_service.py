from app.api.schemas.user import UserCreate, UserFromDb
from app.core.security import hash_password

from app.exceptions.auth_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.utils.uow import IUnitOfWork


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register_user(self, user: UserCreate):
        async with self.uow:
            existing_user = await self.uow.user_repos.find_by_username(user.username)
            if existing_user:
                print(f"Raising UserAlreadyExistsError__________________________________________________________")  # Добавьте отладочное сообщение
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
