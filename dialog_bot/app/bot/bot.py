import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.methods import DeleteWebhook
from faststream.nats import NatsBroker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.handlers import get_routers
from app.bot.handlers.admin import router as admin_router
from app.bot.middlewares import (
    DbSessionMiddleware,
    IsAdminMiddleware,
    RepositoryMiddleware,
    SkipBotMiddleware,
    ThrottlingMiddleware,
    UserSaverMiddleware,
)
from config import config, init_logger

logger = logging.getLogger(__name__)


async def main():
    await init_logger()

    logger.info("Create Postgres engine...")
    engine = create_async_engine(url=str(config.pg_db.dsn), echo=config.pg_db.is_echo)
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    logger.info("Create Redis Storage...")
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
        ),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    logger.info("Create Nats Broker...")
    broker = NatsBroker(servers=config.nats.servers, no_echo=config.nats.no_echo)

    logger.info("Starting Bot...")
    bot = Bot(
        token=config.tg_bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)
    dp.include_routers(*get_routers())

    dp.update.outer_middleware(SkipBotMiddleware())
    dp.message.middleware(ThrottlingMiddleware(throttle_time=1.0))
    dp.update.middleware(DbSessionMiddleware(Sessionmaker))
    dp.update.middleware(RepositoryMiddleware())
    dp.update.middleware(UserSaverMiddleware(broker=broker))
    admin_router.message.middleware(IsAdminMiddleware())
    admin_router.callback_query.middleware(IsAdminMiddleware())

    async with broker:
        await broker.start()
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot, config=config)
