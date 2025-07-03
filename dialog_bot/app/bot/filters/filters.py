from aiogram.filters import BaseFilter
from aiogram.types import Message

from config.config_reader import Config

config: Config = Config.load_config()


class ForumFilter(BaseFilter):
    async def __call__(self, message: Message):
        return (
            message.chat.id == config.basic_ids.forum_id and message.message_thread_id
        )


class NotForumFilter(BaseFilter):
    async def __call__(self, message: Message):
        return message.chat.id != config.basic_ids.forum_id
