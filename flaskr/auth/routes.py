from flask import Blueprint, redirect, render_template, url_for
from flaskr.auth.forms import IngresarForm, RegistroForm

bp = Blueprint("auth", __name__)


@bp.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    form = IngresarForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        return redirect(url_for("auth.ingresar"))

    return render_template("auth/ingresar.html", form=form)


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()

    return render_template("auth/registro.html", form=form)
