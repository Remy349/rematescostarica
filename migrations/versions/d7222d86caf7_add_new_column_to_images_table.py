"""Add new column to images table

Revision ID: d7222d86caf7
Revises: cee4a8773045
Create Date: 2022-07-27 20:19:36.088249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7222d86caf7'
down_revision = 'cee4a8773045'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('relative_path_image', sa.String(length=140), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'relative_path_image')
    # ### end Alembic commands ###