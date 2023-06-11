from flask_login import current_user, login_user, logout_user
from flaskr import db
from flask import Blueprint, flash, redirect, render_template, session, url_for
from sqlalchemy.exc import NoResultFound
from flaskr.auth.forms import IngresarForm, RegistroForm
from flaskr.helpers import clear_form_data_session, generate_code

from flaskr.models.course import Course
from flaskr.models.person import Person
from flaskr.models.student import Student

bp = Blueprint("auth", __name__)


@bp.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    clear_form_data_session()

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

            if user.is_admin is True:
                login_user(user, remember=remember_me)
                return redirect(url_for("admin.dashboard"))
            elif user.is_admin is False:
                student = db.session.execute(
                    db.select(Student).filter(Student.person_id.like(user.id))
                ).scalar_one()

                if student.is_active is True:
                    login_user(user, remember=remember_me)

                    session["student_code"] = student.student_code

                    return redirect(
                        url_for(
                            "user.dashboard",
                            student_code=student.student_code,
                        )
                    )
                elif student.is_active is False:
                    flash("Cuenta suspendida temporalmente!", "error")
                    return redirect(url_for("auth.ingresar"))
        except NoResultFound:
            flash("Usuario no registrado!", "error")

    return render_template(
        "auth/ingresar.html",
        form=form,
        title="Ingresar",
    )


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistroForm()

    courses = db.session.execute(db.select(Course)).scalars().all()

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

    return render_template(
        "auth/registro.html",
        form=form,
        title="Registro",
        courses=courses,
    )


@bp.route("/registro/realizar-compra/<payment_code>", methods=["GET"])
def registro_realizar_compra(payment_code):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if (
        session.get("payment_code") is None
        or session.get("payment_code") != payment_code
    ):
        return redirect(url_for("auth.registro"))

    return render_template(
        "auth/realizar-compra.html",
        title="Realizar Compra",
    )


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

    clear_form_data_session()

    return render_template(
        "auth/compra-finalizada.html",
        title="Compra Finalizada",
    )


@bp.route("/cerrar-sesion", methods=["GET"])
def cerrar_sesion():
    if session.get("course_code") is not None:
        session.pop("course_code", None)
    session.pop("student_code", None)

    logout_user()
    return redirect(url_for("auth.ingresar"))
