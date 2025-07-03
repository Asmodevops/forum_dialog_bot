import asyncio
import logging

from faststream import FastStream
from faststream.nats import NatsBroker

from config import config, init_logger
from handlers import get_routers

logger = logging.getLogger(__name__)


async def main():
    await init_logger()

    broker = NatsBroker(servers=config.nats.servers, no_echo=config.nats.no_echo)
    broker.include_routers(*get_routers())

    app = FastStream(broker)
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
