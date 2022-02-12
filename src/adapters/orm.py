import uuid

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql as sa_psql
from sqlalchemy.orm import registry, sessionmaker

mapper_registry = registry()


restaurant = sa.Table(
    'restaurant',
    mapper_registry.metadata,
    sa.Column('id', sa_psql.UUID(as_uuid=True),
              primary_key=True, default=uuid.uuid4)
)

restaurant_table = sa.Table(
    'restaurant_table',
    mapper_registry.metadata,
    sa.Column('id', sa_psql.UUID(as_uuid=True),
              primary_key=True, default=uuid.uuid4),
    sa.Column('index', sa.Integer, nullable=False),
    sa.Column('restaurant_id', sa.ForeignKey('restaurant.id'), nullable=False)
)

menu_item = sa.Table(
    'menu_item',
    mapper_registry.metadata,
    sa.Column('id', sa_psql.UUID(as_uuid=True),
              primary_key=True, default=uuid.uuid4),
    sa.Column('title', sa.String(256), nullable=False),
    sa.Column('description', sa.String(1024)),
    sa.Column('price_value', sa.DECIMAL, nullable=False),
    sa.Column('restaurant_id', sa.ForeignKey(
        'restaurant.id', ondelete='CASCADE',
    ), nullable=False)
)

order = sa.Table(
    'order',
    mapper_registry.metadata,
    sa.Column('id', sa_psql.UUID(as_uuid=True),
              primary_key=True, default=uuid.uuid4),
    sa.Column('table_id',
              sa.ForeignKey('restaurant_table.id'), nullable=False),
    sa.Column('total_price_value', sa.DECIMAL, nullable=False),
    sa.Column('restaurant_id', sa.ForeignKey('restaurant.id'), nullable=False)
)

order_item = sa.Table(
    'order_item',
    mapper_registry.metadata,
    sa.Column('id', sa_psql.UUID(as_uuid=True),
              primary_key=True, default=uuid.uuid4),
    sa.Column('menu_item_id', sa.ForeignKey('menu_item.id'), nullable=False),
    sa.Column('order_id', sa.ForeignKey('order.id'), nullable=False),
    sa.Column('quantity', sa.SmallInteger, nullable=False)
)


def get_sa_sessionmaker() -> sessionmaker:
    from settings import get_postgres_uri

    engine = create_engine(get_postgres_uri())
    mapper_registry.metadata.create_all(engine)
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )
