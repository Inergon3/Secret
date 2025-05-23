"""empty message

Revision ID: c495a0c6aa7a
Revises: 
Create Date: 2025-04-16 20:31:22.477167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = 'c495a0c6aa7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('secrets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('secret', sa.LargeBinary(), nullable=False),
        sa.Column('passphrase', sa.String(), nullable=False),
        sa.Column('secret_key', sa.UUID(), nullable=False),
        sa.Column('get_secret', sa.Boolean(), nullable=False),
        sa.Column('del_secret', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('secret_key')
    )
    op.create_table('add_secrets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_secret', sa.Integer(), nullable=False),
        sa.Column('time_added', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['id_secret'], ['secrets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('get_secrets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_secret', sa.Integer(), nullable=False),
        sa.Column('time_get', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['id_secret'], ['secrets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('delete_secrets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_secret', sa.Integer(), nullable=False),
        sa.Column('time_delited', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['id_secret'], ['secrets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('delete_secrets')
    op.drop_table('get_secrets')
    op.drop_table('add_secrets')
    op.drop_table('secrets')
    # ### end Alembic commands ###
