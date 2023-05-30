from flask_login import current_user, login_user, logout_user
from flaskr import db
from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy.exc import NoResultFound
from flaskr.auth.forms import IngresarForm, RegistroForm

from flaskr.models.person import Person

bp = Blueprint("auth", __name__)


@bp.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = IngresarForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        try:
            user = db.session.execute(
                db.select(Person).filter_by(email=email)
            ).scalar_one()

            if not user.check_password(password):
                flash("Contraseña incorrecta!", "error")
                return redirect(url_for("auth.ingresar"))

            login_user(user, remember=remember_me)

            if user.is_admin is True:
                return "Admin"
            else:
                return "Student"
        except NoResultFound:
            flash("Usuario no registrado!", "error")

    return render_template("auth/ingresar.html", form=form)


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistroForm()

    return render_template("auth/registro.html", form=form)


@bp.route("/cerrar-sesion", methods=["GET"])
def cerrar_sesion():
    logout_user()
    return redirect(url_for("auth.ingresar"))
