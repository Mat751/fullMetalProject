"""Initial migration.

Revision ID: e61e4d09b0b4
Revises: 905760cea27a
Create Date: 2022-08-20 18:27:18.779070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e61e4d09b0b4'
down_revision = '905760cea27a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('iscritti', sa.Column('provincia', sa.String(length=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('iscritti', 'provincia')
    # ### end Alembic commands ###
