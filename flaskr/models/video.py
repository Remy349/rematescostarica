import sqlalchemy as sa
from flaskr import db


class Video(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    video_name = sa.Column(sa.String(160), nullable=False)
    video_url = sa.Column(sa.String(300), nullable=False)
    video_desc = sa.Column(sa.String(600))
    video_code = sa.Column(sa.String(20))

    cycle_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("cycle.id", ondelete="CASCADE"),
    )

    def __repr__(self):
        return f"""
            video:
                id: {self.id},
        """
