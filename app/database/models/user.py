from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    age: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str]
    hashed_password: Mapped[bytes]
