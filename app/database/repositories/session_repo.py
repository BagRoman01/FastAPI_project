from sqlalchemy import select, delete, and_
from app.database.models.sessions import Session
from app.database.repositories.repository_base import Repository


class SessionRepository(Repository):
    model = Session

    async def get_session_by_refresh_token(self, refresh_token: str):
        query_exec = await self.session.execute(select(self.model).where(self.model.refresh_token == refresh_token))
        return query_exec.scalars().first()

    async def delete_session_by_refresh_token_and_fingerprint(
            self,
            refresh_token: str,
            fingerprint: str
    ):
        print(fingerprint)
        print(refresh_token)

        query_exec = await self.session.execute(
            delete(self.model).where(
                and_(
                    self.model.refresh_token == refresh_token,
                    self.model.fingerprint == fingerprint
                )
            )
        )
        return query_exec

    async def clear_user_sessions(self, user_id: int):
        query_exec = await self.session.execute(delete(self.model).where(self.model.user_id == user_id))
        return query_exec

    async def get_sessions_by_user_id(self, user_id: int):
        query_exec = await self.session.execute(select(self.model).where(self.model.user_id == user_id))
        return query_exec.scalars().all()
