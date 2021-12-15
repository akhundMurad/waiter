import os


def get_postgres_uri() -> str:
    host = os.environ.get('DB_HOST', 'db')
    port = os.environ.get('DB_PORT', 5432)
    password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
