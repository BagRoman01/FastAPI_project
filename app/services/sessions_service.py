from app.api.schemas.session import Session, SessionCreate
from app.utils.uow import IUnitOfWork


class SessionsService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_all_user_sessions(self, user_id: int) -> list[Session]:
        query_exec = await self.uow.session_repos.get_sessions_by_user_id(user_id)
        return [Session.model_validate(session) for session in query_exec]

    async def get_session_by_refresh_token(self, refresh_token: str) -> Session:
        async with self.uow:
            session: Session = await self.uow.session_repos.get_session_by_refresh_token(refresh_token)
            if session:
                return Session.model_validate(session)

    async def add_session(self, session: SessionCreate):
        async with self.uow:
            user_sessions = await self.get_all_user_sessions(session.user_id)
            if len(user_sessions) >= 3:
                print(f"user {session.user_id} sessions have been deleted")
                await self.uow.session_repos.clear_user_sessions(session.user_id)

            query_exec = await self.uow.session_repos.add_one(session.model_dump())
            result = Session.model_validate(query_exec)

            await self.uow.commit()
            print(f"Session {result.id} created")
            return result

