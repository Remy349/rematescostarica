from flaskr import app, db
from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, url_for, session, flash
from helpers import login_required

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

    print(total_data_info)

    return render_template("admin/usuario_admin.html", admin_user=admin_user, videos=videos, users=users, \
                           total_data_info=total_data_info)
