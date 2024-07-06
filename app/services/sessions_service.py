from app.utils.uow import IUnitOfWork


class SessionsService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
