from flaskr import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from helpers import login_required
from openpyxl import Workbook

from flaskr.models import Admin, Users, Videos

@app.route("/iniciar_sesion_admin", methods=["GET", "POST"])
def iniciar_sesion_admin():
    """ Funcion para el inicio de sesion del usuario admin """
    if request.method == "GET":
        if "username" in session:
            return redirect(url_for('usuario_admin'))
        else:
            return render_template("admin/iniciar_sesion_admin.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        errors = None

        admin_user = Admin.query.filter_by(username=username).first()

        if admin_user is None:
            errors = "Nombre de usuario incorrecto!"
        elif not check_password_hash(admin_user.password, password):
            errors = "Contraseña incorrecta!"

        if errors is None:
            session["user_id"] = admin_user.id
            session["username"] = admin_user.username
            session["gravatar"] = admin_user.gravatar
            session.permanent = True
            return redirect(url_for("usuario_admin"))

        if errors:
            flash(errors)
            return redirect(url_for("iniciar_sesion_admin"))

@app.route("/perfil/usuario_admin", methods=["GET"])
@login_required
def usuario_admin():
    """ Funcion para mostrar el perfil del usuario admin del sitio """
    username = session.get("username")

    admin_user = Admin.query.filter_by(username=username).first()
    videos = Videos.query.all()
    users = Users.query.all()

    total_users = 0
    payment_completed_users = 0
    payment_uncompleted_users = 0

    for user in users:
        total_users = total_users + 1

        if user.payment_completed == "Sin Adquirir":
            payment_uncompleted_users = payment_uncompleted_users + 1

        if user.payment_completed == "Adquirido":
            payment_completed_users = payment_completed_users + 1

    total_data_info = {
        "total_users": total_users,
        "payment_completed_users": payment_completed_users,
        "payment_uncompleted_users": payment_uncompleted_users,
    }

    return render_template("admin/usuario_admin.html", admin_user=admin_user, videos=videos, users=users, \
                           total_data_info=total_data_info)

@app.route("/perfil/usuario_admin/editar_perfil", methods=["GET", "POST"])
@login_required
def editar_perfil_admin():
    """ Ruta para poder editar el perfil del usuario admin """
    if request.method == "GET":
        username = session.get("username")

        admin_user = Admin.query.filter_by(username=username).first()

        return render_template("admin/editar_perfil_admin.html", admin_user=admin_user)
    elif request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email_adress = request.form["email_adress"]
        password_value = request.form["password"]

        username = session.get("username")

        admin_user = Admin.query.filter_by(username=username).first()
        videos = Videos.query.all()
        users = Users.query.all()

        total_users = 0
        payment_completed_users = 0
        payment_uncompleted_users = 0

        for user in users:
            total_users = total_users + 1

            if user.payment_completed == "Sin Adquirir":
                payment_uncompleted_users = payment_uncompleted_users + 1

            if user.payment_completed == "Adquirido":
                payment_completed_users = payment_completed_users + 1

        total_data_info = {
            "total_users": total_users,
            "payment_completed_users": payment_completed_users,
            "payment_uncompleted_users": payment_uncompleted_users,
        }

        if password_value == "" or password_value == " ":
            admin_user.firstname = firstname
            admin_user.lastname = lastname
            admin_user.email_adress = email_adress
        else:
            admin_user.firstname = firstname
            admin_user.lastname = lastname
            admin_user.email_adress = email_adress
            password = generate_password_hash(password_value)
            admin_user.password = password

        db.session.add(admin_user)
        db.session.commit()

        return render_template("admin/usuario_admin.html", admin_user=admin_user, videos=videos, users=users, \
                               total_data_info=total_data_info)

@app.route("/create_file", methods=["GET"])
def create_file():
    """ Crear archivo excel con los datos de los usuarios """
    users = Users.query.all()
    wb = Workbook()
    user_array = []

    hoja = wb.active
    hoja.title = "Registro de usuarios"

    for user in users:
        user_array.append((
            user.firstname,
            user.lastname,
            user.username,
            user.phonenumber,
            user.email_adress,
            user.adress,
            user.postal_code,
            user.payment_completed
        ))

    hoja.append(("PrimerNombre", "PrimerApellido", "NombreDeUsuario", "NumeroTelefonico", \
                 "DireccionDeCorreo", "Direccion", "CodigoPostal", "EstadoDelCurso"))

    for item in user_array:
        hoja.append(item)

    wb.save("flaskr/static/files/Usuarios.xlsx")

    return jsonify({"message": "Creating file..."})
