from flask import Blueprint, render_template
from flaskr import db
from flaskr.helpers import clear_form_data_session

from flaskr.models.course import Course

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    courses = db.session.execute(db.select(Course)).scalars().all()

    clear_form_data_session()

    return render_template("main/index.html", courses=courses)
