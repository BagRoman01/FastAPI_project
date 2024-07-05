from sqlalchemy import select
from app.database.models.user import User
from repository_base import Repository


class UserRepository(Repository):
    model = User

    async def find_by_username(self, username: str) -> model:
        model = self.model
        query_exec = await self.session.execute(select(model).where(model.username == username))
        result = query_exec.scalars().first()
        return result
