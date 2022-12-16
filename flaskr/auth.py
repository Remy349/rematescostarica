import os
from flaskr import app, db
from flask import render_template, redirect, url_for, request, session, flash, jsonify
from hashlib import md5
from werkzeug.security import generate_password_hash

from flaskr.models import Users, Registro
from helpers import login_required


@app.route("/registro", methods=["GET", "POST"])
@login_required
def registro():
    if request.method == "GET":
        return render_template("routes/pasarela.html")
    elif request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email_adress = request.form["email_adress"]
        phonenumber = request.form["phonenumber"]
        course_type = request.form["course_type"]

        errors = None

        registro = Registro.query.filter_by(email_adress=email_adress).first()

        if registro is not None:
            errors = "Ese correo ya esta registrado!"

        if errors is None:
            payment_completed = "Sin Adquirir"
            print(firstname, lastname, phonenumber, email_adress, course_type, payment_completed)

            new_registro = Registro(firstname=firstname.lower(), lastname=lastname.lower(),
                                    phonenumber=phonenumber, email_adress=email_adress.lower(),
                                    course_type=course_type, payment_completed=payment_completed)

            db.session.add(new_registro)
            db.session.commit()

            session["email_adress"] = email_adress

            if course_type == "vivo":
                return redirect(url_for("comprar_curso"))
            elif course_type == "pregrabado":
                return redirect(url_for("comprar_curso_two"))

        if errors:
            return redirect(url_for("registro"))


@app.route("/registrate", methods=["GET", "POST"])
def registrate():
    """ Funcion para manejar y realizar el proceso de registro de un nuevo usuario """
    if request.method == "GET":
        if "username" in session:
            username = session.get("username")
            admin_username =os.getenv("ADMIN_USERNAME")

            if username == admin_username:
                return redirect(url_for("usuario_admin"))
            else:
                return redirect(url_for("perfil", username=username))
        else:
            return render_template("auth/registrate.html")
    elif request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        phonenumber = request.form["phonenumber"]
        email_adress = request.form["email_adress"]
        adress = request.form["adress"]
        postal_code = request.form["postal_code"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        errors = None

        user = Users.query.filter_by(username=username).first()

        if user is not None:
            errors = f"'{username}' ya esta registrado! Usa otro!"

        if errors is None:
            gravatar = md5(email_adress.lower().encode("utf-8")).hexdigest()
            payment_completed = "Sin Adquirir"

            new_user = Users(firstname=firstname.lower(), lastname=lastname.lower(), username=username, phonenumber=phonenumber, \
                email_adress=email_adress.lower(), adress=adress, postal_code=postal_code, gravatar=gravatar, payment_completed=payment_completed
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print(new_user)

            return redirect(url_for("iniciar_sesion"))

        if errors:
            flash(errors)
            return redirect(url_for("registrate"))

@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    """ Funcion para realizar el inicio de sesion de cada usuario """
    if request.method == "GET":
        if "username" in session:
            username = session.get("username")
            admin_username =os.getenv("ADMIN_USERNAME")

            if username == admin_username:
                return redirect(url_for("usuario_admin"))
            else:
                return redirect(url_for("perfil", username=username))
        else:
            return render_template("auth/iniciar_sesion.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        errors = None

        user = Users.query.filter_by(username=username).first()

        if user is None:
            errors = "Nombre de usuario incorrecto!"
        elif not user.check_password(password):
            errors = "Contraseña incorrecta!"

        if errors is None:
            session["user_id"] = user.id
            session["username"] = user.username
            session["gravatar"] = user.gravatar
            session.permanent = True
            return redirect(url_for("perfil", username=username))

        if errors:
            flash(errors)
            return redirect(url_for("iniciar_sesion"))

@app.route("/cerrar_sesion", methods=["GET"])
def cerrar_sesion():
    """ Funcion para realizar el cierre de sesion """
    session.clear()
    return redirect(url_for("index"))

@app.route("/iniciar_sesion/new_password", methods=["GET", "POST"])
def new_password():
    """ Funcion para la modificacion de contraseña en caso que el usuario la olvidara """
    if request.method == "GET":
        return render_template("auth/new_password.html")
    elif request.method == "POST":
        email_adress = request.form["email"]
        message = None
        response = None

        find_user = Users.query.filter_by(email_adress=email_adress).first()

        if find_user is None:
            message = "Dirección E-Mail no registrada!"
            response = 404
        else:
            session["email_temp"] = find_user.email_adress
            message = find_user.username
            response = 200

        return jsonify({
            "message": message,
            "response": response
        })

@app.route("/create_new_password", methods=["POST"])
def create_new_password():
    """ Funcion para la creacion de la nueva contraseña """
    password_value = request.form["password"]
    email_adress = session.get("email_temp")
    user_update = Users.query.filter_by(email_adress=email_adress).first()

    password_hash = generate_password_hash(password_value)

    user_update.password_hash = password_hash

    db.session.add(user_update)
    db.session.commit()

    session.pop("email_temp", None)

    return redirect(url_for("iniciar_sesion"))
