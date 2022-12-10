"""empty message

Revision ID: 599a5de00802
Revises: 63b5f372c9f2
Create Date: 2022-12-09 22:43:54.295516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '599a5de00802'
down_revision = '63b5f372c9f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=25), nullable=False),
    sa.Column('lastname', sa.String(length=25), nullable=False),
    sa.Column('phonenumber', sa.String(length=25), nullable=False),
    sa.Column('email_adress', sa.String(length=160), nullable=False),
    sa.Column('course_type', sa.String(length=25), nullable=False),
    sa.Column('payment_completed', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_adress')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registro')
    # ### end Alembic commands ###
