import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from faststream.nats import NatsBroker

from app.bot.repository.users import UserRepository
from app.bot.schemas import UserSchema

logger = logging.getLogger(__name__)


class UserSaverMiddleware(BaseMiddleware):
    def __init__(self, broker: NatsBroker):
        self.broker = broker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        config = data.get("config")
        tg_user: User = data.get("event_from_user")
        if tg_user:
            try:
                user: UserSchema = UserSchema(
                    telegram_id=tg_user.id,
                    first_name=tg_user.first_name,
                    last_name=tg_user.last_name,
                    full_name=tg_user.full_name,
                    username=tg_user.username,
                )
                await self.broker.publish(
                    message=user,
                    stream=config.fix_user_consumer.stream,
                    subject=config.fix_user_consumer.subject,
                )

            except Exception as e:
                logger.error(f"Error while saving user: {e}")

                user_repo: UserRepository = data.get("user_repo")
                user = await user_repo.create_user(
                    telegram_id=tg_user.id,
                    first_name=tg_user.first_name,
                    last_name=tg_user.last_name,
                    full_name=tg_user.full_name,
                    username=tg_user.username,
                )

        return await handler(event, data)
