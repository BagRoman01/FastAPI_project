from sqlalchemy import select, delete
from app.database.models.sessions import Session
from repository_base import Repository


class SessionRepository(Repository):
    model = Session

    async def get_session_by_refresh_token(self, refresh_token: str):
        query_exec = await self.session.execute(select(self.model).where(self.model.refresh_token == refresh_token))
        return query_exec.scalars().first()

    async def clear_user_sessions(self, user_id: int):
        query_exec = await self.session.execute(delete(self.model).where(self.model.user_id == user_id))
        return query_exec

    async def get_sessions_by_user_id(self, user_id: int):
        query_exec = await self.session.execute(select(self.model).where(self.model.user_id == user_id))
        return query_exec.scalars().all()
