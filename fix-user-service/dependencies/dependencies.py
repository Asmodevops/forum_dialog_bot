from faststream import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_async_session
from repository import UserRepository


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return UserRepository(session)
