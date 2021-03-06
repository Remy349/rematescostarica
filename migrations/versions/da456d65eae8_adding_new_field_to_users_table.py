"""Adding new field to users table

Revision ID: da456d65eae8
Revises: 3fc8bed30730
Create Date: 2022-04-17 19:00:10.807783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da456d65eae8'
down_revision = '3fc8bed30730'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('gravatar', sa.String(length=120), nullable=False))
    op.create_unique_constraint(None, 'users', ['gravatar'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'gravatar')
    # ### end Alembic commands ###
