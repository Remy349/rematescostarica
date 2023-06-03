from flask_login import current_user, login_user, logout_user
from flaskr import db
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import NoResultFound
from flaskr.auth.forms import IngresarForm, RegistroForm
from flaskr.helpers import generate_code

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
                return redirect(url_for("admin.dashboard"))
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

    if form.validate_on_submit():
        firstname = form.firstname.data
        first_lastname = form.first_lastname.data
        second_lastname = form.second_lastname.data
        email = form.email.data
        phone_number = form.phone_number.data

        payment_code = generate_code()

        session["firstname"] = firstname
        session["first_lastname"] = first_lastname
        session["second_lastname"] = second_lastname
        session["email"] = email
        session["phone_number"] = phone_number
        session["payment_code"] = payment_code

        return redirect(
            url_for(
                "auth.registro_realizar_compra",
                payment_code=payment_code,
            )
        )

    return render_template("auth/registro.html", form=form)


@bp.route("/registro/realizar-compra/<payment_code>", methods=["GET"])
def registro_realizar_compra(payment_code):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if (
        session.get("payment_code") is None
        or session.get("payment_code") != payment_code
    ):
        return redirect(url_for("auth.registro"))

    return render_template("auth/realizar-compra.html")


@bp.route(
    "/registro/realizar-compra/<payment_code>/compra-finalizada",
    methods=["GET"],
)
def registro_compra_finalizada(payment_code):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if (
        session.get("payment_code") is None
        or session.get("payment_code") != payment_code
    ):
        return redirect(url_for("main.index"))

    session.clear()

    return render_template("auth/compra-finalizada.html")


@bp.route("/cerrar-sesion", methods=["GET"])
def cerrar_sesion():
    logout_user()
    return redirect(url_for("auth.ingresar"))
