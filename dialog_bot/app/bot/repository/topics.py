from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.bot.repository.base import BaseRepository
from database.models import Topic


class TopicRepository(BaseRepository[Topic]):
    def __init__(self, session):
        super().__init__(session, Topic)

    async def create_topic(self, thread_id, user_id) -> bool:
        stmt = (
            insert(Topic)
            .values(
                thread_id=thread_id,
                user_id=user_id,
            )
            .on_conflict_do_update(
                index_elements=["user_id"],
                set_={
                    "thread_id": thread_id,
                },
            )
        )
        await self.session.execute(stmt)
        await self.commit_or_rollback()
        return True

    async def get_thread_id_by_user_id(self, user_id: int) -> Optional[Dict[str, int]]:
        stmt = select(Topic.thread_id).where(Topic.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.mappings().first()

    async def get_user_id_by_thread_id(
        self, thread_id: int
    ) -> Optional[Dict[str, int]]:
        stmt = select(Topic.user_id).where(Topic.thread_id == thread_id)
        result = await self.session.execute(stmt)
        return result.mappings().first()
