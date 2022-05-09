import os
from flaskr import app, db
from flask import render_template, redirect, url_for, request, session, flash
from hashlib import md5

from flaskr.models import Users

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

            new_user = Users(firstname=firstname, lastname=lastname, username=username, phonenumber=phonenumber, \
                email_adress=email_adress, adress=adress, postal_code=postal_code, gravatar=gravatar, payment_completed=payment_completed
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
