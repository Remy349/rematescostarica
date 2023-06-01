import sqlalchemy as sa
from flaskr import db


class Change(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    change_price = sa.Column(sa.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"""
            change:
                id: {self.id},
                change_price: {self.change_price},
        """
