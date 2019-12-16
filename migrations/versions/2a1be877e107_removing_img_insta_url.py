"""Removing img_insta_url

Revision ID: 2a1be877e107
Revises: 6ddc43f74fef
Create Date: 2019-12-15 14:18:53.023734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a1be877e107'
down_revision = '6ddc43f74fef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'img_insta_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('img_insta_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
