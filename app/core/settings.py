import logging
from os import environ
from typing import Any, Dict, Final, List

from pydantic import BaseConfig


class Settings(BaseConfig):
    API_PREFIX: str = environ.get("API_PREFIX", "/api")
    APP_NAME: str = environ.get("APP_NAME", "Applifting")
    DEBUG: bool = environ.get("DEBUG") == "True"
    POSTGRES_DB: str = environ.get("POSTGRES_DB", "")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "")
    OFFERS_MS_URL: str = environ.get("OFFERS_MS_URL", "")
    OFFERS_REFRESH_DELAY_SECONDS: int = int(
        environ.get("OFFERS_REFRESH_DELAY_SECONDS", 60)
    )
    OFFERS_TOKEN_LIFETIME_SECONDS: int = int(
        environ.get("OFFERS_TOKEN_LIFETIME_SECONDS", 900)
    )
    DB_ASYNC_CONNECTION_STR: str = environ.get("DB_ASYNC_CONNECTION_STR", "")

    logging.getLogger().setLevel(logging.DEBUG)
    FORMAT = "%(asctime)s %(message)s"
    logging.basicConfig(format=FORMAT)
