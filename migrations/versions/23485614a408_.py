"""empty message

Revision ID: 23485614a408
Revises: 2323df4bbe17
Create Date: 2015-10-20 00:39:40.471801

"""

# revision identifiers, used by Alembic.
revision = '23485614a408'
down_revision = '2323df4bbe17'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_confirmed')
    ### end Alembic commands ###
