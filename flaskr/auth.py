from flaskr import app, db
from flask import render_template, redirect, url_for, request, session, flash

from flaskr.models import Users

@app.route("/registrate", methods=["GET", "POST"])
def registrate():
    """ Funcion para manejar y realizar el proceso de registro de un nuevo usuario """
    if request.method == "GET":
        if "username" in session:
            return redirect(url_for("cursos"))
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

        if username == user.username:
            errors = f"'{username}' ya esta registrado! Usa otro!"
        elif email_adress == user.email_adress:
            errors = f"Dirección de correo ya ocupado!"

        if errors is None:
            new_user = Users(firstname=firstname, lastname=lastname, username=username, phonenumber=phonenumber, \
                email_adress=email_adress, adress=adress, postal_code=postal_code
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("iniciar_sesion"))

        if errors:
            flash(errors)
            return redirect(url_for("registrate"))

@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    """ Funcion para realizar el inicio de sesion de cada usuario """
    if request.method == "GET":
        if "username" in session:
            return redirect(url_for("cursos"))
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
            session.permanent = True
            return redirect(url_for("cursos"))

        if errors:
            flash(errors)
            return redirect(url_for("iniciar_sesion"))

@app.route("/cerrar_sesion", methods=["GET"])
def cerrar_sesion():
    """ Funcion para realizar el cierre de sesion """
    session.clear()
    return redirect(url_for("index"))
