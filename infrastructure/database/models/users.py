from typing import Optional

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, default=None
    )
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True, default=None)

    topic: Mapped["Topic"] = relationship("Topic", back_populates="user")
