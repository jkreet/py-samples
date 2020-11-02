"""empty message

Revision ID: 275d739f5ac3
Revises: 4e55f7016a73
Create Date: 2020-06-30 00:00:41.003887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '275d739f5ac3'
down_revision = '4e55f7016a73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('year', sa.String(length=4), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car', 'year')
    # ### end Alembic commands ###
