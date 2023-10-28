"""add table Users, Permissions, Task

Revision ID: eb1fdc62eb85
Revises: 
Create Date: 2023-10-28 00:26:43.252519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb1fdc62eb85'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_permission',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('codename', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('codename'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users_user',
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=30), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_user_created_at'), 'users_user', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_user_email'), 'users_user', ['email'], unique=True)
    op.create_index(op.f('ix_users_user_username'), 'users_user', ['username'], unique=True)
    op.create_table('task_task',
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('owner_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_task_created_at'), 'task_task', ['created_at'], unique=False)
    op.create_index(op.f('ix_task_task_description'), 'task_task', ['description'], unique=False)
    op.create_index(op.f('ix_task_task_title'), 'task_task', ['title'], unique=False)
    op.create_table('users_userpermission',
    sa.Column('codename', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['codename'], ['users_permission.codename'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('codename', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_userpermission')
    op.drop_index(op.f('ix_task_task_title'), table_name='task_task')
    op.drop_index(op.f('ix_task_task_description'), table_name='task_task')
    op.drop_index(op.f('ix_task_task_created_at'), table_name='task_task')
    op.drop_table('task_task')
    op.drop_index(op.f('ix_users_user_username'), table_name='users_user')
    op.drop_index(op.f('ix_users_user_email'), table_name='users_user')
    op.drop_index(op.f('ix_users_user_created_at'), table_name='users_user')
    op.drop_table('users_user')
    op.drop_table('users_permission')
    # ### end Alembic commands ###
