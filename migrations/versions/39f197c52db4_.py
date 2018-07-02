"""empty message

Revision ID: 39f197c52db4
Revises: 3343f3d2a9c2
Create Date: 2018-07-02 18:37:01.030194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39f197c52db4'
down_revision = '3343f3d2a9c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('text', sa.String(length=2048), nullable=True))
    op.drop_column('article', 'content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('content', sa.VARCHAR(length=2048), autoincrement=False, nullable=True))
    op.drop_column('article', 'text')
    # ### end Alembic commands ###
