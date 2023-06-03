import sqlalchemy as sa
from flaskr import db

student_course = db.Table(
    "student_course",
    sa.Column("student_id", sa.Integer, sa.ForeignKey("student.id")),
    sa.Column("course_id", sa.Integer, sa.ForeignKey("course.id")),
)
