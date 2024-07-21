from datetime import datetime
from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey, DateTime
from app.database.models.user import User


class Session(Base):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    refresh_token: Mapped[str]
    fingerprint: Mapped[str]
    exp_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    @staticmethod
    def get_primary_key():
        return Session.id
