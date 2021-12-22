import uuid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as sa_psql
from sqlalchemy.orm import relationship, registry

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
    sa.Column('restaurant_id', sa.ForeignKey('restaurant.id'),
              primary_key=True)
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

order_and_menu_item_association_table = sa.Table(
    'order_and_menu_item_association_table',
    mapper_registry.metadata,
    sa.Column('order_id', sa.ForeignKey('order.id'), primary_key=True),
    sa.Column('menu_item_id', sa.ForeignKey('menu_item.id'), primary_key=True)
)

order = sa.Table(
    'order',
    mapper_registry.metadata,
    sa.Column('id', sa_psql.UUID(as_uuid=True),
              primary_key=True, default=uuid.uuid4),
    sa.Column('table_index',
              sa.ForeignKey('restaurant_table.index'), nullable=False),
    sa.Column('total_price_value', sa.DECIMAL, nullable=False),
    sa.Column('restaurant_id', sa.ForeignKey('restaurant.id'), nullable=False)
)
