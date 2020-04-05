import logging
import os
from dataclasses import dataclass


@dataclass
class Settings:
    TWITTER_CONSUMER_KEY: str = os.environ["TWITTER_CONSUMER_KEY"]
    TWITTER_CONSUMER_SECRET: str = os.environ["TWITTER_CONSUMER_SECRET"]
    TWITTER_QUERY: str = os.environ["TWITTER_QUERY"]
    TWITTER_TWEETS_NUMBER: int = int(os.environ["TWITTER_TWEETS_NUMBER"])
    TWITTER_TASK_PERIOD: int = int(os.environ["TWITTER_TASK_PERIOD"])
    LOGGING_LEVEL: int = int(os.environ.get("LOGGING_LEVEL"))
    PG_USER: str = os.environ["PG_USER"]
    PG_PASSWORD: str = os.environ["PG_PASSWORD"]
    PG_DATABASE: str = os.environ["PG_DATABASE"]
    PG_HOST: str = os.environ["PG_HOST"]
    PG_PORT: int = 5432


@dataclass
class SettingsDev(Settings):
    LOGGING_LEVEL: int = os.environ.get("LOGGING_LEVEL") or logging.DEBUG


def build_pg_url(settings: Settings) -> str:
    return f"postgresql://{settings.PG_USER}:{settings.PG_PASSWORD}" \
                   f"@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DATABASE}"
