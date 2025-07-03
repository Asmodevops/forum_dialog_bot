from environs import Env
from pydantic import BaseModel, PostgresDsn


class NatsConfig(BaseModel):
    servers: list[str]
    no_echo: bool


class NatsFixUserConsumerConfig(BaseModel):
    subject: str
    stream: str
    durable_name: str


class PgDB(BaseModel):
    dsn: PostgresDsn
    is_echo: bool


class Config(BaseModel):
    nats: NatsConfig
    fix_user_consumer: NatsFixUserConsumerConfig
    pg_db: PgDB

    @classmethod
    def load_config(cls, path: str | None = None) -> "Config":
        env = Env()
        env.read_env(path)
        return cls(
            nats=NatsConfig(
                servers=env.list("NATS_SERVERS"),
                no_echo=env.bool("NO_ECHO"),
            ),
            fix_user_consumer=NatsFixUserConsumerConfig(
                subject=env.str("NATS_FIX_USER_CONSUMER_SUBJECT"),
                stream=env.str("NATS_FIX_USER_CONSUMER_STREAM"),
                durable_name=env.str("NATS_FIX_USER_CONSUMER_DURABLE_NAME"),
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
        )


config = Config.load_config()
