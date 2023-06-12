import sqlalchemy as sa
from flaskr import db


class Material(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    material_name = sa.Column(sa.String(160), nullable=False)
    material_path = sa.Column(sa.String(300))
    material_code = sa.Column(sa.String(20))

    video_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("video.id", ondelete="CASCADE"),
    )

    def __repr__(self):
        return f"""
            material:
                id: {self.id},
        """
