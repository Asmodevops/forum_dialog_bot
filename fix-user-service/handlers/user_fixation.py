from faststream import Depends, Logger
from faststream.nats import JStream, NatsRouter
from faststream.nats.annotations import NatsMessage

from config import config
from dependencies.dependencies import get_user_repository
from repository.users import UserRepository
from schemas import UserSchema

router = NatsRouter()


@router.subscriber(
    subject=config.fix_user_consumer.subject,
    stream=JStream(name=config.fix_user_consumer.stream),
    durable=config.fix_user_consumer.durable_name,
)
async def user_fixation_handler(
    body: dict,
    msg: NatsMessage,
    logger: Logger,
    user_repo: UserRepository = Depends(get_user_repository),
):
    logger.info(f"Received: {body}")

    user: UserSchema = UserSchema.model_validate(body)
    await user_repo.create_user(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        username=user.username,
    )
    await msg.ack()
