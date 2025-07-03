from database.models import User
from sqlalchemy.dialects.postgresql import insert

from repository.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(session, User)

    async def create_user(
        self, telegram_id, first_name, last_name, full_name, username
    ) -> User:
        stmt = (
            insert(User)
            .values(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                username=username,
            )
            .on_conflict_do_update(
                index_elements=["telegram_id"],
                set_={
                    "first_name": first_name,
                    "last_name": last_name,
                    "full_name": full_name,
                    "username": username,
                },
            )
            .returning(User)
        )
        result = await self.session.execute(stmt)
        await self.commit_or_rollback()
        return result.scalar_one()
