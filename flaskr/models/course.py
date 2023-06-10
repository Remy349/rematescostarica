import sqlalchemy as sa
from flaskr import db


class Course(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    course_name = sa.Column(sa.String(160), nullable=False)
    course_basic_desc = sa.Column(sa.String(600))
    course_desc = sa.Column(sa.String(600))
    course_price = sa.Column(sa.Numeric(10, 2), nullable=False)
    course_code = sa.Column(sa.String(20))
    secure_url = sa.Column(sa.String(160))
    public_id = sa.Column(sa.String(160))

    cycles = db.relationship("Cycle", backref="course", lazy="dynamic")

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
