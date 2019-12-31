"""Reposts

Revision ID: 76d7e9381f58
Revises: 6be1035ab153
Create Date: 2019-12-28 22:26:25.674157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76d7e9381f58'
down_revision = '6be1035ab153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reposts',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('managed_instagram_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['managed_instagram_account_id'], ['managed_instagram_accounts.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reposts')
    # ### end Alembic commands ###
