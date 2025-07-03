from environs import Env
from pydantic import BaseModel, PostgresDsn, SecretStr


class TgBot(BaseModel):
    token: SecretStr


class PgDB(BaseModel):
    dsn: PostgresDsn
    is_echo: bool


class BasicIds(BaseModel):
    admin_id: int
    forum_id: int


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int


class NatsConfig(BaseModel):
    servers: list[str]
    no_echo: bool


class NatsFixUserConsumerConfig(BaseModel):
    subject: str
    stream: str


class Config(BaseModel):
    pg_db: PgDB
    tg_bot: TgBot
    basic_ids: BasicIds
    redis: RedisConfig
    nats: NatsConfig
    fix_user_consumer: NatsFixUserConsumerConfig

    @classmethod
    def load_config(cls, path: str | None = None) -> "Config":
        env = Env()
        env.read_env(path)
        return cls(
            tg_bot=TgBot(
                token=SecretStr(env.str("BOT_TOKEN")),
            ),
            pg_db=PgDB(
                dsn=PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=env.str("POSTGRES_USER"),
                    password=env.str("POSTGRES_PASSWORD"),
                    host=env.str("DB_HOST"),
                    port=env.int("DB_PORT"),
                    path=env.str("POSTGRES_DB"),
                ),
                is_echo=env.bool("ECHO"),
            ),
            basic_ids=BasicIds(
                admin_id=env.int("ADMIN_ID"),
                forum_id=env.int("FORUM_ID"),
            ),
            redis=RedisConfig(
                host=env.str("REDIS_HOST"),
                port=env.int("REDIS_PORT"),
                db=env.int("REDIS_DB"),
            ),
            nats=NatsConfig(
                servers=env.list("NATS_SERVERS"), no_echo=env.bool("NO_ECHO")
            ),
            fix_user_consumer=NatsFixUserConsumerConfig(
                subject=env.str("NATS_FIX_USER_CONSUMER_SUBJECT"),
                stream=env.str("NATS_FIX_USER_CONSUMER_STREAM"),
            ),
        )


config = Config.load_config()
