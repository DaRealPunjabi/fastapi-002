"""add foreign key to posts table

Revision ID: 9886ce11ca19
Revises: dca103e33e7e
Create Date: 2023-05-01 12:15:01.545357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9886ce11ca19'
down_revision = 'dca103e33e7e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
