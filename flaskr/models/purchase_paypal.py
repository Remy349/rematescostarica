import sqlalchemy as sa
from flaskr import db
from datetime import datetime


class PurchasePaypal(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    purchase_gross_amount = sa.Column(sa.Numeric(10, 2), nullable=False)
    purchase_paypal_fee = sa.Column(sa.Numeric(10, 2), nullable=False)
    purchase_net_amount = sa.Column(sa.Numeric(10, 2), nullable=False)
    purchase_date = sa.Column(sa.DateTime, default=datetime.utcnow)

    student_id = sa.Column(sa.Integer, sa.ForeignKey("student.id"))
    course_id = sa.Column(sa.Integer, sa.ForeignKey("course.id"))

    def __repr__(self):
        return f"""
            purchase_paypal:
                id: {self.id},
                purchase_date: {self.purchase_date},
        """
