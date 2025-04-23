"""Update datetime fields to use UTC without timezone

Revision ID: 06afbe8b2304
Revises: bfdc4b7d336d
Create Date: 2025-04-24 00:38:12.160170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '06afbe8b2304'
down_revision: Union[str, None] = 'bfdc4b7d336d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Изменяем тип created_at на DateTime без timezone
    op.alter_column(
        'user',
        'created_at',
        type_=sa.DateTime(timezone=False),
        server_default=text("(NOW() AT TIME ZONE 'UTC')"),
        nullable=False
    )
    
    # Изменяем тип updated_at на DateTime без timezone
    op.alter_column(
        'user',
        'updated_at',
        type_=sa.DateTime(timezone=False),
        server_default=text("(NOW() AT TIME ZONE 'UTC')"),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Возвращаем тип created_at на DateTime с timezone
    op.alter_column(
        'user',
        'created_at',
        type_=sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False
    )
    
    # Возвращаем тип updated_at на DateTime с timezone
    op.alter_column(
        'user',
        'updated_at',
        type_=sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False
    )
