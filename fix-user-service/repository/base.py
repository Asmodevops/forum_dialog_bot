from abc import ABC
from typing import Generic, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def __init__(self, session, model: Type[T]):
        self.session = session
        self.model = model

    async def commit_or_rollback(self):
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ValueError(f"Database error: {e}") from e
