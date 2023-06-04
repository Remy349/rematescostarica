import sqlalchemy as sa
from flaskr import db

from flaskr.models.student_course import student_course


class Course(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    course_name = sa.Column(sa.String(160), nullable=False)
    course_desc = sa.Column(sa.String(600))
    course_price = sa.Column(sa.String(20), nullable=False)
    course_code = sa.Column(sa.String(20))
    secure_url = sa.Column(sa.String(160))
    public_id = sa.Column(sa.String(160))

    purchases_paypal = db.relationship(
        "PurchasePaypal",
        backref="course",
        lazy="dynamic",
    )

    def __repr__(self):
        return f"""
            course:
                id: {self.id},
        """
