from app.services.authorization.sessions_service import SessionsService
from app.services.authorization.users_service import UsersService
from app.api.dependencies import uow_dep


class AuthService:
    def __init__(self, uow: uow_dep):
        self.session_service = SessionsService(uow)
        self.users_service = UsersService(uow)

