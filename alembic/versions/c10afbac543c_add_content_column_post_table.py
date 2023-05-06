"""add content column post table

Revision ID: c10afbac543c
Revises: 23d44627d083
Create Date: 2023-05-01 11:57:42.070489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c10afbac543c'
down_revision = '23d44627d083'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', 
                  sa.Column('content', sa.String(), nullable=False)
                  )
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
