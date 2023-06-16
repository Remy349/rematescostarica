from flask import Blueprint, render_template
from flaskr import db
from flaskr.helpers import clear_form_data_session

from flaskr.models.course import Course
from flaskr.models.faq import Faq

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    courses = db.session.execute(db.select(Course)).scalars().all()
    faqs = db.session.execute(db.select(Faq)).scalars().all()

    clear_form_data_session()

    return render_template(
        "main/index.html",
        courses=courses,
        faqs=faqs,
    )
