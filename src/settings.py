import os


def get_postgres_uri() -> str:
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 5432)
    password = os.environ.get('DB_PASSWORD', 'waiter')
    db_name = os.environ.get('DB_NAME', 'waiter')
    user = os.environ.get('DB_USER', 'waiter')
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'