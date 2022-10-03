"""creating users table

Revision ID: 3fc8bed30730
Revises: 
Create Date: 2022-04-11 15:06:08.590290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3fc8bed30730'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=25), nullable=False),
    sa.Column('lastname', sa.String(length=25), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('phonenumber', sa.String(length=25), nullable=False),
    sa.Column('email_adress', sa.String(length=160), nullable=False),
    sa.Column('adress', sa.String(length=160), nullable=True),
    sa.Column('postal_code', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=160), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_adress'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
