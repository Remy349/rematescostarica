"""empty message

Revision ID: aad84d708840
Revises: 
Create Date: 2023-06-09 23:17:31.260060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aad84d708840'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('change',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('change_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_change'))
    )
    op.create_table('course',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_name', sa.String(length=160), nullable=False),
    sa.Column('course_basic_desc', sa.String(length=600), nullable=True),
    sa.Column('course_desc', sa.String(length=600), nullable=True),
    sa.Column('course_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('course_code', sa.String(length=20), nullable=True),
    sa.Column('secure_url', sa.String(length=160), nullable=True),
    sa.Column('public_id', sa.String(length=160), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_course'))
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.String(length=20), nullable=False),
    sa.Column('first_lastname', sa.String(length=20), nullable=False),
    sa.Column('second_lastname', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=280), nullable=False),
    sa.Column('password_hash', sa.String(length=180), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_person'))
    )
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_person_email'), ['email'], unique=True)

    op.create_table('cycle',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cycle_name', sa.String(length=160), nullable=False),
    sa.Column('cycle_desc', sa.String(length=600), nullable=True),
    sa.Column('cycle_code', sa.String(length=20), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name=op.f('fk_cycle_course_id_course')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cycle'))
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('phone_number', sa.String(length=40), nullable=False),
    sa.Column('student_code', sa.String(length=30), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('joined_in', sa.DateTime(), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], name=op.f('fk_student_person_id_person')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_student')),
    sa.UniqueConstraint('person_id', name=op.f('uq_student_person_id'))
    )
    op.create_table('purchase_paypal',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('purchase_gross_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('purchase_paypal_fee', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('purchase_net_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('purchase_date', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name=op.f('fk_purchase_paypal_course_id_course')),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_purchase_paypal_student_id_student')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_purchase_paypal'))
    )
    op.create_table('student_course',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name=op.f('fk_student_course_course_id_course')),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name=op.f('fk_student_course_student_id_student'))
    )
    op.create_table('video',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('video_name', sa.String(length=160), nullable=False),
    sa.Column('video_url', sa.String(length=300), nullable=False),
    sa.Column('video_desc', sa.String(length=600), nullable=True),
    sa.Column('video_code', sa.String(length=20), nullable=True),
    sa.Column('cycle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cycle_id'], ['cycle.id'], name=op.f('fk_video_cycle_id_cycle'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_video'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    op.drop_table('student_course')
    op.drop_table('purchase_paypal')
    op.drop_table('student')
    op.drop_table('cycle')
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_person_email'))

    op.drop_table('person')
    op.drop_table('course')
    op.drop_table('change')
    # ### end Alembic commands ###
