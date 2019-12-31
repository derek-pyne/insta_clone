"""Unique handle in accounts

Revision ID: 2d23f031b1e5
Revises: 76d7e9381f58
Create Date: 2019-12-31 13:49:13.174741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d23f031b1e5'
down_revision = '76d7e9381f58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'managed_instagram_accounts', ['handle'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'managed_instagram_accounts', type_='unique')
    # ### end Alembic commands ###
