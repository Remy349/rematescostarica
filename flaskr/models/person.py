import sqlalchemy as sa
from flaskr import db, login_manager
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Person(UserMixin, db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    firstname = sa.Column(sa.String(20), nullable=False)
    first_lastname = sa.Column(sa.String(20), nullable=False)
    second_lastname = sa.Column(sa.String(20), nullable=False)
    email = sa.Column(sa.String(280), nullable=False, unique=True, index=True)
    password_hash = sa.Column(sa.String(180))
    is_admin = sa.Column(sa.Boolean, default=False)

    student = db.relationship(
        "Student",
        backref="person",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon"

    def __repr__(self):
        return f"""
            person:
                id: {self.id},
                is_admin: {self.is_admin},
        """


@login_manager.user_loader
def load_user(id):
    return db.session.execute(
        db.select(Person).filter_by(id=int(id)),
    ).scalar_one()
