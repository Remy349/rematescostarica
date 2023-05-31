from flask import redirect, render_template, url_for
from flaskr import db
from flask_login import current_user, login_required
from flaskr.admin.base import bp
from flaskr.admin.forms import AddUpdateCourse

from flaskr.models.course import Course


@bp.route("/cursos", methods=["GET"])
@login_required
def cursos():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    courses = db.session.execute(db.select(Course)).scalars().all()

    return render_template(
        "admin/cursos.html",
        page="Cursos",
        title="Cursos",
        courses=courses,
    )


@bp.route("/cursos/agregar-curso", methods=["GET", "POST"])
@login_required
def cursos_agregar_curso():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = AddUpdateCourse()

    return render_template(
        "admin/cursos/agregar-curso.html",
        form=form,
        title="Agregar curso",
        page="Agregar curso",
    )
