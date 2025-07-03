import logging

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from app.bot.filters.filters import ForumFilter
from app.bot.repository.topics import TopicRepository
from app.bot.schemas.topic import TopicUserIdSchema

router = Router(name="admin router")

logger = logging.getLogger(__name__)


@router.message(ForumFilter())
async def response_msg(message: Message, topic_repo: TopicRepository):
    raw_user_id = await topic_repo.get_user_id_by_thread_id(
        thread_id=message.message_thread_id
    )
    if not raw_user_id:
        logger.info(f"No user_id found for thread_id {message.message_thread_id}")
        return

    topic_user_id: TopicUserIdSchema = TopicUserIdSchema.model_validate(raw_user_id)
    try:
        await message.send_copy(chat_id=topic_user_id.user_id)
    except TelegramBadRequest as e:
        logger.warning(f"Can't send message to user_id {topic_user_id.user_id}\n\n{e}")
    except Exception as e:
        logger.warning(f"Unexpected error\n\n{e}")
