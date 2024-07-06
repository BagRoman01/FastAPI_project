from app.api.schemas.user import UserCreate, UserFromDb
from app.utils.uow import IUnitOfWork


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserCreate):
        async with self.uow:
            query_exec = await self.uow.user_repos.add_one(user.model_dump())
            result = UserFromDb.model_validate(query_exec)
            await self.uow.commit()
            return result

