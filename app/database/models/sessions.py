from datetime import datetime
from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey
from app.database.models.user import User


class Session(Base):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    refresh_token: Mapped[str]
    fingerprint: Mapped[str]
    exp_at: Mapped[float]
    created_at: Mapped[datetime]

    @staticmethod
    def get_primary_key():
        return Session.id
