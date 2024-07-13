from typing import Annotated
from app.api.schemas.others import Tokens
from app.core.security import get_fingerprint, get_tokens_from_cookie
from app.services.authorization.sessions_service import SessionsService
from app.services.authorization.users_service import UsersService
from app.utils.uow import UnitOfWork, IUnitOfWork
from fastapi import Depends

uow_dep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


async def get_users_service(uow: uow_dep) -> UsersService:
    return UsersService(uow)


async def get_sessions_service(uow: uow_dep) -> SessionsService:
    return SessionsService(uow)

fingerprint_dep = Annotated[str, Depends(get_fingerprint)]
users_service_dep = Annotated[UsersService, Depends(get_users_service)]
sessions_service_dep = Annotated[SessionsService, Depends(get_sessions_service)]
tokens_dep = Annotated[Tokens, Depends(get_tokens_from_cookie)]