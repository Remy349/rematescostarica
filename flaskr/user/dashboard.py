from flask import redirect, render_template, url_for
from flaskr import db
from flask_login import current_user, login_required
from flaskr.user.base import bp

from flaskr.models.student import Student


@bp.route("/dashboard/<student_code>", methods=["GET"])
@login_required
def dashboard(student_code):
    student = db.session.execute(
        db.select(Student).filter_by(student_code=student_code)
    ).scalar_one()

    if current_user.id != student.person_id:
        return redirect(
            url_for(
                "user.dashboard",
                student_code=student_code,
            )
        )

    return render_template(
        "user/index.html",
        page="Dashboard",
        title="Dashboard",
    )
