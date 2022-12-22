"""empty message

Revision ID: 62e668b69cb6
Revises: 65078e5d4230
Create Date: 2022-12-21 20:01:28.033769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62e668b69cb6'
down_revision = '65078e5d4230'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('course_type', sa.String(length=25), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'course_type')
    # ### end Alembic commands ###
