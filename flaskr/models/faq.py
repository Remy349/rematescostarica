import sqlalchemy as sa
from flaskr import db


class Faq(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    question = sa.Column(sa.String(600), nullable=False)
    answer = sa.Column(sa.String(900), nullable=False)

    def __repr__(self):
        return f"""
            id: {self.id},
        """
