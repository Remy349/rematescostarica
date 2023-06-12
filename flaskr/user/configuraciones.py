from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from flaskr.models.person import Person
from flaskr.user.base import bp
from flaskr import db
from flaskr.user.forms import UpdatePassword

from flaskr.models.student import Student


@bp.route("/dashboard/<student_code>/configuraciones", methods=["GET", "POST"])
@login_required
def configuraciones(student_code):
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

    form = UpdatePassword()

    if form.validate_on_submit():
        password = form.password.data

        user = db.session.execute(
            db.select(Person).filter_by(id=current_user.id)
        ).scalar_one()

        user.set_password(password=password)

        db.session.add(user)
        db.session.commit()

        flash("Contraseña actualizada exitosamente!", "success")

        return redirect(
            url_for(
                "user.configuraciones",
                student_code=student_code,
            )
        )

    return render_template(
        "user/configuraciones.html",
        page="Configuraciones",
        title="Configuraciones",
        form=form,
    )
