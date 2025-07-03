from sqlalchemy import BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    thread_id: Mapped[int] = mapped_column(
        Integer, unique=True, index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="SET NULL"),
        unique=True,
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="topic", passive_deletes=True
    )
