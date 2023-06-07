from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from flaskr import db
from flaskr.admin.base import bp
from flaskr.admin.forms import UpdatePassword
from flaskr.models.person import Person


@bp.route("/configuraciones", methods=["GET", "POST"])
@login_required
def configuraciones():
    if current_user.is_admin is False:
        return redirect(url_for("main.index"))

    form = UpdatePassword()

    if form.validate_on_submit():
        password = form.password.data

        user = db.session.execute(
            db.select(Person).filter_by(id=current_user.id, is_admin=True)
        ).scalar_one()

        user.set_password(password=password)

        db.session.add(user)
        db.session.commit()

        flash("Contraseña actualizada exitosamente!", "success")

        return redirect(url_for("admin.configuraciones"))

    return render_template(
        "admin/configuraciones.html",
        page="Configuraciones",
        title="Configuraciones",
        form=form,
    )
