from contextlib import suppress

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ForumTopic, Message

from app.bot.filters.filters import NotForumFilter
from app.bot.repository.topics import TopicRepository
from app.bot.schemas.topic import TopicThreadIdSchema
from config.config_reader import Config

router = Router(name="general router")


@router.message(NotForumFilter())
async def cmd_start(
    message: Message, bot: Bot, config: Config, topic_repo: TopicRepository
):
    forum_id = config.basic_ids.forum_id
    raw_thread_id = await topic_repo.get_thread_id_by_user_id(
        user_id=message.from_user.id
    )
    if raw_thread_id:
        topic_thread_id: TopicThreadIdSchema = TopicThreadIdSchema.model_validate(
            raw_thread_id
        )
        with suppress(TelegramBadRequest):
            await message.send_copy(
                chat_id=forum_id,
                message_thread_id=topic_thread_id.thread_id,
            )
            return

    topic: ForumTopic = await bot.create_forum_topic(
        chat_id=forum_id,
        name=f"Dialogue_with_{message.from_user.full_name}_{message.from_user.id}",
    )
    if not await topic_repo.create_topic(
        thread_id=topic.message_thread_id, user_id=message.from_user.id
    ):
        await message.answer(
            text="Произошла ошибка при создании нового топика. Попробуйте отправить любое сообщение еще раз."
        )
        return

    await bot.send_message(
        chat_id=forum_id,
        message_thread_id=topic.message_thread_id,
        text=f"Пользователь <b>{message.from_user.full_name}</b> ({message.from_user.id}) начал диалог.\n\n",
    )
    await message.send_copy(
        chat_id=forum_id,
        message_thread_id=topic.message_thread_id,
    )
