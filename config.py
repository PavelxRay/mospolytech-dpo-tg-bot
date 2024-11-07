import os
from dataclasses import dataclass

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
    return cfg


config = setup_config()
