"""empty message

Revision ID: 6bcf6323f738
Revises: 7f956490573f
Create Date: 2020-06-30 02:11:59.827955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bcf6323f738'
down_revision = '7f956490573f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'car', 'location', ['current_location_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'car', type_='foreignkey')
    # ### end Alembic commands ###
