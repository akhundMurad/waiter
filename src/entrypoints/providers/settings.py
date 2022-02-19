from functools import lru_cache

from pydantic import BaseSettings

from settings import Settings


def settings_provider() -> BaseSettings:
    ...


@lru_cache
def get_settings() -> Settings:
    return Settings()
