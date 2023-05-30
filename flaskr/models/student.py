import sqlalchemy as sa
from flaskr import db
from datetime import datetime


class Student(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    phone_number = sa.Column(sa.String(40), nullable=False)
    student_code = sa.Column(sa.String(30))
    joined_in = sa.Column(sa.DateTime, default=datetime.utcnow)

    person_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("person.id"),
        unique=True,
        nullable=False,
    )

    def __repr__(self):
        return f"""
            student:
                id: {self.id},
        """
