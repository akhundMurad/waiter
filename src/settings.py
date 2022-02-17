from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_password: str = 'waiter'
    postgres_name: str = 'waiter'
    postgres_user: str = 'waiter'

    api_host: str = 'localhost'
    api_port: int = 8000
