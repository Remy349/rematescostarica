import sqlalchemy as sa
from flaskr import db


class Cycle(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    cycle_name = sa.Column(sa.String(160), nullable=False)
    cycle_desc = sa.Column(sa.String(600))
    cycle_code = sa.Column(sa.String(20))

    course_id = sa.Column(sa.Integer, sa.ForeignKey("course.id"))

    videos = db.relationship(
        "Video",
        backref="cycle",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"""
            cycle:
                id: {self.id},
        """
