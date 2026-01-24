"""add_performance_indexes

Revision ID: 89489375e8e2
Revises: 6dd4fa64541a
Create Date: 2026-01-16 21:25:28.514159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89489375e8e2'
down_revision: Union[str, None] = '6dd4fa64541a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add index on conversations.updated_at for faster sorting
    op.create_index(
        'ix_conversations_updated_at',
        'conversations',
        ['updated_at'],
        unique=False
    )

    # Add index on messages.created_at for chronological ordering
    op.create_index(
        'ix_messages_created_at',
        'messages',
        ['created_at'],
        unique=False
    )

    # Add index on tasks.title for faster search (if needed in future)
    # This may already exist from previous migrations, so check first
    try:
        op.create_index(
            'ix_tasks_title',
            'tasks',
            ['title'],
            unique=False
        )
    except Exception:
        # Index already exists, skip
        pass


def downgrade() -> None:
    # Remove indexes in reverse order
    op.drop_index('ix_messages_created_at', table_name='messages')
    op.drop_index('ix_conversations_updated_at', table_name='conversations')

    try:
        op.drop_index('ix_tasks_title', table_name='tasks')
    except Exception:
        # Index didn't exist, skip
        pass
