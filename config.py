import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class BotConfig:
    token: str


@dataclass
class DatabaseConfig:
    host: str
    port: str
    user: str
    password: str
    db_name: str
    url: Optional[str] = None


@dataclass
class Config:
    bot: BotConfig
    database: DatabaseConfig


def setup_config() -> Config:
    load_dotenv()
    cfg = Config(
        bot=BotConfig(
            token=os.getenv("TG_BOT_TOKEN")
        ),
        database=DatabaseConfig(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            db_name=os.getenv("DB_NAME"),
        )
    )
    db = cfg.database
    cfg.database.url = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db_name}"
    return cfg


config = setup_config()
