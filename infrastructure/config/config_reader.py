from environs import Env
from pydantic import BaseModel, PostgresDsn


class PgDB(BaseModel):
    dsn: PostgresDsn
    is_echo: bool


class Config(BaseModel):
    pg_db: PgDB

    @classmethod
    def load_config(cls, path: str | None = None) -> "Config":
        env = Env()
        env.read_env(path)
        return cls(
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
            )
        )


config = Config.load_config()
